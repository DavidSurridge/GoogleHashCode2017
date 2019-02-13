const validation = require('../lib/validation');
const scoring = require('../lib/score');
const { copySolution, getRandomInteger, getRandomIntegerNotInArray } = require('../lib/helpers');

const addRandomVideoInRandomCacheServer = (solution, input) => {
  let randomCacheServer;
  let randomVideo;
  let tempSolution;
  let isNewEntry = false;
  do {
    tempSolution = copySolution(solution);
    randomCacheServer = getRandomInteger(0, input.nbCacheServers - 1);
    randomVideo = getRandomInteger(0, input.nbVideos - 1);
    if (!Array.isArray(tempSolution.cacheServers[randomCacheServer])) {
      tempSolution.cacheServers[randomCacheServer] = [];
    }
    startTime = Date.now();
    if (tempSolution.cacheServers[randomCacheServer].indexOf(randomVideo) === -1) {
      tempSolution.cacheServers[randomCacheServer].push(randomVideo);
      isNewEntry = true;
    } else {
      isNewEntry = false;
    }
  } while (isNewEntry && !validation.isSolutionValid(solution, input));
  solution.cacheServers = tempSolution.cacheServers;
  
  return {
    cacheServer: randomCacheServer,
    video: randomVideo
  };
};

const getInitialSolutionByFillingWithVideos = (solution, input) => {
  let videoAdded = false;
  for (let i=0; i<input.nbCacheServers; i++) {
    let size = 0;
    let done = false;
    solution.cacheServers[i] = [];
    do {
      videoAdded = getRandomIntegerNotInArray(0, input.nbVideos, solution.cacheServers[i]);
      if (videoAdded && size + input.videos[videoAdded] <= input.cacheServerCapacity) {
        size += input.videos[videoAdded];
        solution.cacheServers[i].push(videoAdded);
      } else {
        done = true;
      }
    } while (!done);
  }
  solution.score = scoring.computeScore(solution, input);
};

const getInitialSolutionByAddingOneVideo = (solution, input) => {
  addRandomVideoInRandomCacheServer(solution, input);
  solution.score = scoring.computeScore(solution, input);
};

const getInitialSolutionFromInput = (solution, input) => {
  Object.keys(input.solution.cacheServers)
    .forEach(cacheServerId => {
      solution.cacheServers[cacheServerId] = [...input.solution.cacheServers[cacheServerId]];
    });
  solution.score = scoring.computeScore(solution, input);
}

const getVariantByAddingOneVideo = (solution, input) => {
  const addedBit = addRandomVideoInRandomCacheServer(solution, input); 
  solution.score = scoring.computeScore(solution, input, { type: 'ADD', payload: addedBit });
};

const getVariantBySwappingOneVideo = (solution, input) => {
  let randomCacheServer;
  let previousVideo;
  let newVideo;
  let randomVideoIndex;
  let tempSolution;
  let isValid = false;
  let nbAttempts = 0;
  const nbAttemptsMax = 1000;
  let swappedBit;
  do {
    tempSolution = copySolution(solution);
    randomCacheServer = getRandomInteger(0, input.nbCacheServers - 1);
    if (!tempSolution.cacheServers[randomCacheServer]) {
      tempSolution.cacheServers[randomCacheServer] = [];
    }
    if (tempSolution.cacheServers[randomCacheServer].length) {
      randomVideoIndex = getRandomInteger(0, tempSolution.cacheServers[randomCacheServer].length - 1);
      newVideo = getRandomIntegerNotInArray(0, input.nbVideos - 1, tempSolution.cacheServers[randomCacheServer]);
      if (newVideo) {
        previousVideo = tempSolution.cacheServers[randomCacheServer][randomVideoIndex];
        tempSolution.cacheServers[randomCacheServer][randomVideoIndex] = newVideo;
        isValid = true;
      } else {
        isValid = false;
      }
    } else {
      isValid = false;
    }
    nbAttempts++;
  } while (nbAttempts <= nbAttemptsMax && !isValid);
  if (isValid) {
    solution.cacheServers = tempSolution.cacheServers;
    solution.lastChange = Date.now();
    swappedBit = {
      cacheServer: randomCacheServer,
      previousVideo,
      newVideo
    };
  } else {
    swappedBit = false;
  }
  solution.score = scoring.computeScore(solution, input, { type: 'SWAP', payload: swappedBit });      
};

module.exports = {
  getInitialSolutionByAddingOneVideo,
  getInitialSolutionByFillingWithVideos,
  getInitialSolutionFromInput,
  getVariantByAddingOneVideo,
  getVariantBySwappingOneVideo
};