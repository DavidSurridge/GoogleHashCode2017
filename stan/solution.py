from reader import Reader as ReaderMixIn
from writer import Writer as WriterMixIn


class Solution(ReaderMixIn, WriterMixIn):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculate_max_latency()

    def calculate_max_latency(self):
        self.max_latency = 0
        for r in self.requests.values():
            full_latency = r.requests * self.endpoints[r.endpoint].data_center_latency
            self.max_latency += full_latency

        self.savings = 0
        print('Worst case latency is %s' % self.max_latency)

    def __repr__(self):
        return '<Solution savings=%s>' % self.savings

    def remove_endpoint(self, endpoint_id):
        print('Removing endpoint %s' % endpoint_id)
        del self.endpoints[endpoint_id]

    def remove_request(self, request_id):
        print('Removing request %s' % request_id)
        del self.requests[request_id]

    def remove_video(self, video_id):
        print('Removing video %s' % video_id)
        del self.videos[video_id]

    def get_caches_for_endpoint(self, endpoint):
        for cache_id in endpoint.connections.keys():
            cache = self.cache_servers[cache_id]
            if cache.free_space == 0:
                continue
            yield cache_id

    def get_all_endpoint_for_cache(self, cache_id):
        for endpoint_id, endpoint in self.endpoints.items():
            if cache_id in endpoint.connections:
                yield endpoint_id

    def get_all_requests_for_endpoint(self, endpoint_id):
        for req_id, request in self.requests.items():
            if request.endpoint == endpoint_id:
                yield req_id

    def get_saved_latency(self, request_id, endpoint_id, cache_id):
        req = self.requests[request_id]
        end = self.endpoints[endpoint_id]
        worst_latency = req.requests * end.data_center_latency
        cache_latency = req.requests * end.connections[cache_id]
        return worst_latency - cache_latency

    def add_video_to_cache(self, cache_id, video_id):
        """
        1) remove video from all related endpoints.video_requested sets
        2) while iterating by endpoints - calculate latency we save
        3) add video to cache server
        """
        video = self.videos[video_id]
        cache = self.cache_servers[cache_id]
        if video.size > cache.free_space:
            print('Cannot put video %s(%s) into cache %s(%s): not enough space left on device' % (video_id, video, cache_id, cache))
            return

        if video_id in cache.videos_stored_ids:
            print('Cannot put video %s(%s) into cache %s(%s): video is already there' % (video_id, video, cache_id, cache))
            return

        print('Adding video %s(%s) to cache %s(%s)' % (video_id, video, cache_id, cache))
        cache.videos_stored.add(video)
        cache.videos_stored_ids.add(video_id)
        print('Updated cache: %s' % cache)

        for endpoint_id in self.get_all_endpoint_for_cache(cache_id):
            endpoint = self.endpoints[endpoint_id]
            endpoint.videos_requested.remove(video_id)
            print('Updated endpoint: %s' % endpoint)
            for request_id in self.get_all_requests_for_endpoint(endpoint_id):
                request = self.requests.get(request_id)
                if request.video == video_id:
                    # request is satisfied! we've saved some latency here
                    saved_latency = self.get_saved_latency(request_id, endpoint_id, cache_id)
                    print("Saved latency %s" % saved_latency)
                    self.savings +=saved_latency
