const fs = require('fs');
const parse = require('./lib/parse');
const { formatTime } = require('./lib/helpers');
const HIGHEST_SCORE = require('./lib/highest_score');

const strategy = require('./strategies/hillclimbing');

const {
  getInitialSolutionByAddingOneVideo,
  getInitialSolutionByFillingWithVideos,
  getInitialSolutionFromInput,
  getVariantByAddingOneVideo,
  getVariantBySwappingOneVideo,
} = require('./strategies/methods');



const inputDirname = './inputs/';
const inputs = [];

// Parse input files
const filenames = fs.readdirSync(inputDirname);
filenames.forEach(filename => {
  const content = fs.readFileSync(inputDirname + filename, 'utf-8');
  
  inputs.push(parse.parseInputContent(content, filename));
});

// Augment inputs
inputs.forEach(input => {
  // Compute the total number of requests
  input.nbTotalRequests = input.requests.reduce((acc, request) => acc + request.nbRequests, 0);
  // For each cacheServer, store the list of endpoints connected to it
  input.cacheServers = {};
  input.endpoints.forEach((endpoint, endpointId) => {
    endpoint.cacheServersConnected.forEach(cacheServer => {
      if (!input.cacheServers[cacheServer.id]) {
        input.cacheServers[cacheServer.id] = [];
      }
      input.cacheServers[cacheServer.id].push(endpointId);
    });
  });
});

console.log('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n');
inputs.forEach(input => {
  console.log('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~');
  console.log(input.filename);
  console.log('~~~~~~~~~~~~~~~~~~~~~~~~~');
  const timestamp = Date.now();

  // Strategy #1
  // Initial solution: Add 1 video
  // Variant: Add 1 video
  // strategy.apply(input, getInitialSolutionByAddingOneVideo, getVariantByAddingOneVideo);
  
  // Strategy #2
  // Initial solution: Fill with videos
  // Variant: Swap 1 video
  // strategy.apply(input, getInitialSolutionByFillingWithVideos, getVariantBySwappingOneVideo);
  
  // Strategy #3
  // Hill climbing #1
  // Initial solution: Add 1 video
  // Variant: Add 1 video
  // Hill climbing #2
  // Initial solution: Solution from Hill climbing #1
  // Variant: Swap 1 video
  strategy.apply(input, getInitialSolutionByAddingOneVideo, getVariantByAddingOneVideo);
  strategy.apply(input, getInitialSolutionFromInput, getVariantBySwappingOneVideo);
  

  console.log(`\nScore: ${input.solution.score} / ${HIGHEST_SCORE[input.filename]}`)
  const timeElapsed = Date.now() - timestamp;
  console.log(`\nTime: ${formatTime(timeElapsed)}\n`);
});

console.log('\n\n');
const totalScore = inputs.reduce((acc, input) => {
  console.log(`${input.filename}: ${input.solution.score} / ${HIGHEST_SCORE[input.filename]}`);
  return acc + input.solution.score
}, 0);
console.log(`\nTotal Score: ${totalScore}\n\n`);

