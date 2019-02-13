const { formatTime } = require('./helpers');

const computeScore_Default = (solution, input) => {
  solution.requests = [];
  return Math.floor(
    input.requests
      .reduce((acc, request) => {
        const cacheServersConnectedContainingVideo = input.endpoints[request.endpointId].cacheServersConnected
          .filter(cacheServer => {
            const videosContainedInCacheServer = solution.cacheServers[cacheServer.id];
            return Array.isArray(videosContainedInCacheServer)
              && videosContainedInCacheServer.indexOf(request.videoId) > -1;
          });
          const timeSaved = cacheServersConnectedContainingVideo.length ?
            input.endpoints[request.endpointId].dataCenterLatency - Math.min(...cacheServersConnectedContainingVideo.map(cacheServer => cacheServer.latency)) :
            0;
        solution.requests.push({ timeSaved });
        return acc + (timeSaved * request.nbRequests);
      }, 0)
      * 1000
      / input.nbTotalRequests
    );
};

const computeScore_Swap = (solution, input, payload) => {
  payload.cacheServer
  payload.previousVideo
  payload.newVideo

  const updatedRequests = input.requests
    .filter(request => (
        request.videoId === payload.previousVideo ||
        request.videoId === payload.newVideo 
      ) &&
        Array.isArray(input.cacheServers[payload.cacheServer]) &&
        input.cacheServers[payload.cacheServer].indexOf(request.endpointId) > -1);

  updatedRequests.forEach(request => {
    const endpoint = input.endpoints[request.endpointId];
    const cacheServersConnectedContainingVideo = endpoint.cacheServersConnected.filter(cacheServer => {
      const videosContainedInCacheServer = solution.cacheServers[cacheServer.id];
      return Array.isArray(videosContainedInCacheServer)
        && videosContainedInCacheServer.indexOf(request.videoId) > -1;
    });

    const timeSaved = cacheServersConnectedContainingVideo.length ?
      endpoint.dataCenterLatency - Math.min(...cacheServersConnectedContainingVideo.map(cacheServer => cacheServer.latency)) :
      0;
    solution.requests[request.id].timeSaved = timeSaved;
  });

  return Math.floor(
    input.requests.reduce((acc, request) => acc + request.nbRequests * solution.requests[request.id].timeSaved, 0)
      * 1000
      / input.nbTotalRequests
  );
};

const computeScore_Add = (solution, input, payload) => {
  // console.log(solution.cacheServers);
  // console.log(solution.requests);
  const updatedRequests = input.requests
    .filter(request => request.videoId === payload.video &&
      Array.isArray(input.cacheServers[payload.cacheServer]) &&
      input.cacheServers[payload.cacheServer].indexOf(request.endpointId) > -1);

  updatedRequests.forEach(request => {
    const endpoint = input.endpoints[request.endpointId];
    const cacheServersConnectedContainingVideo = endpoint.cacheServersConnected.filter(cacheServer => {
      const videosContainedInCacheServer = solution.cacheServers[cacheServer.id];
      return Array.isArray(videosContainedInCacheServer)
        && videosContainedInCacheServer.indexOf(request.videoId) > -1;
    });
    const timeSaved = cacheServersConnectedContainingVideo.length ?
      endpoint.dataCenterLatency - Math.min(...cacheServersConnectedContainingVideo.map(cacheServer => cacheServer.latency)) :
      0;
    solution.requests[request.id].timeSaved = timeSaved;
  });
  // console.log('------>');
  // console.log(solution.requests);

  return Math.floor(
    input.requests.reduce((acc, request) => acc + request.nbRequests * solution.requests[request.id].timeSaved, 0)
      * 1000
      / input.nbTotalRequests
  );

};

const computeScore = (solution, input, method = {}) => {
  switch(method.type) {
    case 'ADD':
      return computeScore_Add(solution, input, method.payload);
    case 'SWAP':
      return computeScore_Swap(solution, input, method.payload);
    default:
      return computeScore_Default(solution, input);
  }
};

module.exports = {
  computeScore
};