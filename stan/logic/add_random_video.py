import random


def add_random_video(solution):
    print('--- add_random_video start')
    for _ in range(10):
        endpoint_with_requests = [e for e in solution.endpoints.values() if e.videos_requested]
        if not endpoint_with_requests:
            print('No more requests left')
            break

        random_endpoint = random.choice(endpoint_with_requests)
        random_video_id = random.choice(list(random_endpoint.videos_requested))

        endpoint_caches = [cache_id for cache_id in solution.get_caches_for_endpoint(random_endpoint)]
        if not endpoint_caches:
            print('No suitable cache for endpoint %s' % random_endpoint)
            continue

        random_cache_id = random.choice(endpoint_caches)
        solution.add_video_to_cache(random_cache_id, random_video_id)
    print('--- add_random_video end')
