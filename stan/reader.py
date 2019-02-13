def read_int_line(f):
    return [int(i) for i in f.readline().strip().split(' ')]


class Video:
    def __init__(self, size):
        self.size = size
    
    def __repr__(self):
        return "<Video (%s)>" % self.size


class Endpoint:
    def __init__(self, data_center_latency):
        self.data_center_latency = data_center_latency
        self.connections = {}
        self.videos_requested = set()

    def add_connection(self, cache, latency):
        self.connections[cache] = latency
    
    def __repr__(self):
        return "<Endpoint (%s connections, videos requested: %s)>" % (len(self.connections), self.videos_requested)


class Cache:
    def __init__(self, capacity):
        self.total_capacity = capacity
        self.videos_stored = set()
        self.videos_stored_ids = set()

    @property
    def free_space(self):
        space_taken = sum([v.size for v in self.videos_stored])
        return self.total_capacity - space_taken

    def add_video(self, video):
        if video.size > self.free_space:
            raise RuntimeError("No space left on device %s" % self)
        self.videos_stored.add(video)

    def __repr__(self):
        return "<CacheServer (%s/%s), videos stored: %s>" % (self.free_space, self.total_capacity, self.videos_stored)


class Request:
    def __init__(self, v_id, e_id, requests):
        self.video = v_id
        self.endpoint = e_id
        self.requests = requests

    def __repr__(self):
        return '<Request (video: %s, endpoint: %s, requests: %s)>' % (self.video, self.endpoint, self.requests)


class Reader:

    def _init_caches(self, amount, cache_size):
        self.cache_servers = {}
        for i in range(amount):
            self.cache_servers[i] = Cache(cache_size)

    def _init_videos(self, fin):
        self.videos = {}
        vids = read_int_line(fin)
        for i, vid_size in enumerate(vids):
            self.videos[i] = Video(vid_size)

    def _init_endpoints(self, amount, fin):
        self.endpoints = {}
        for i in range(amount):
            dc_lat, connection_amount = read_int_line(fin)
            endpoint = Endpoint(dc_lat)
            for _ in range(connection_amount):
                cache_server, latency = read_int_line(fin)
                endpoint.add_connection(cache_server, latency)
            self.endpoints[i] = endpoint

    def _init_requests(self, amount, fin):
        self.requests = {}
        for i in range(amount):
            req = Request(*read_int_line(fin))
            self.requests[i] = req
            self.endpoints[req.endpoint].videos_requested.add(req.video)

    def __init__(self, fin):
        # read all required info from the file
        _, n_ends, n_reqs, n_cachs, cache_size = read_int_line(fin)

        self._init_caches(n_cachs, cache_size)
        self._init_videos(fin)
        self._init_endpoints(n_ends, fin)
        self._init_requests(n_reqs, fin)


if __name__ == '__main__':
    reader = Reader(open('me_at_the_retirement_home.in'))
    import ipdb;ipdb.set_trace()
