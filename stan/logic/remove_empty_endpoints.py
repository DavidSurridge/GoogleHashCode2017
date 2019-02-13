def remove_empty_endpoints(solution):
    print('--- remove empty endpoints start')
    videos_from_all_endpoints = set()
    videos_marked_for_removal = set()

    endpoints_keys = list(solution.endpoints.keys())
    for endpoint_id in endpoints_keys:
        endpoint = solution.endpoints[endpoint_id]
        if endpoint.connections:
            videos_from_all_endpoints |= endpoint.videos_requested
            continue

        # we've got empty endpoint here
        # lets remove it from solution
        solution.remove_endpoint(endpoint_id)

        # we also need to remove requests, because we cannot help it
        req_keys = list(solution.requests.keys())
        for req_id in req_keys:
            req = solution.requests[req_id]
            if req.endpoint == endpoint_id:
                videos_marked_for_removal.add(req.video)
                solution.remove_request(req_id)

    diff = videos_marked_for_removal - videos_from_all_endpoints
    for video in diff:
        solution.remove_video(video)
    print('--- remove empty endpoints end')
