const isSolutionValid = (solution, input) => {
  return solution.cacheServers &&
    !Object.keys(solution.cacheServers)
      .map(cacheServerId => solution.cacheServers[cacheServerId])
      .map(videos => videos
        .reduce((acc, videoId) => acc + input.videos[videoId], 0)
      )
      .find(size => size > input.cacheServerCapacity);
};

module.exports = {
  isSolutionValid
};