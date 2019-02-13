const parseInputContent = (content, filename) => {
  const result = {
    filename,
    filesize: content.length,
    nbVideos: 0,
    nbEndpoints: 0,
    nbRequests: 0,
    nbCacheServers: 0,
    cacheServerCapacity: 0,
    videos: [],
    endpoints: [],
    requests: []
  };
  const lines = content.split('\n');
  let lineIndex = 0;
  let line = lines[lineIndex];

  const nextLine = () => { lineIndex++; line = lines[lineIndex]; };
  const toInt = (nb) => parseInt(nb, 10);
  const toIntArray = (line) => line.split(' ').map(toInt);

  // First line
  [
    result.nbVideos,
    result.nbEndpoints,
    result.nbRequests,
    result.nbCacheServers,
    result.cacheServerCapacity
  ] = toIntArray(line);
  nextLine();

  // Video sizes
  result.videos = toIntArray(line);

  // Endpoints
  for (let endpointIndex = 0; endpointIndex < result.nbEndpoints; endpointIndex++) {
    nextLine();
    const endpoint = {
      dataCenterLatency: 0,
      cacheServersConnected: []
    };
    let nbCacheServersConnected = 0;
    [endpoint.dataCenterLatency, nbCacheServersConnected] = toIntArray(line);
    for (let cacheServerIndex = 0; cacheServerIndex < nbCacheServersConnected; cacheServerIndex++) {
      const cacheServer = {};
      nextLine();
      [cacheServer.id, cacheServer.latency] = toIntArray(line);
      endpoint.cacheServersConnected.push(cacheServer);
    }
    result.endpoints.push(endpoint);
  }

  // Requests
  for (let requestIndex = 0; requestIndex < result.nbRequests; requestIndex++) {
    nextLine();
    const request = { id: requestIndex };
    [request.videoId, request.endpointId, request.nbRequests] = toIntArray(line);
    result.requests.push(request);
  }
  return result;
};

module.exports = {
  parseInputContent
};