const getRandomInteger = (minValue, maxValue) => minValue + Math.floor(Math.random() * (maxValue - minValue + 1));

const getRandomIntegerNotInArray = (minValue, maxValue, arr) => {
  if (arr.length <= maxValue - minValue) {
    let value = 0;
    do {
      value = getRandomInteger(minValue, maxValue);
    } while (arr.indexOf(value) > -1);
    return value;
  } else {
    return false;
  }
};

const formatTime = (time) => {
  const milliseconds = time % 1000;
  const timeInSeconds = Math.floor(time / 1000);
  const seconds = timeInSeconds % 60;
  const minutes = Math.floor(timeInSeconds / 60);
  return [
    minutes ? `${minutes}m ` : '',
    seconds ? `${seconds}s ` : '',
    (milliseconds || (!minutes && !seconds)) ? `${milliseconds}ms` : ''
  ].join('');
};

const copySolution = (solution) => {
  const copy = {
    cacheServers: {},
    lastChange: solution.lastChange,
    score: solution.score,
    lastScoreChange: solution.lastScoreChange,
    requests: [...solution.requests.map(request => ({ timeSaved: request.timeSaved }))]
  };
  Object.keys(solution.cacheServers)
    .forEach(cacheServerId => {
      copy.cacheServers[cacheServerId] = [...solution.cacheServers[cacheServerId]];
    });
  return copy;
};

module.exports = {
  getRandomInteger,
  getRandomIntegerNotInArray,
  formatTime,
  copySolution
};