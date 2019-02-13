class Writer:

    def dump(self):
        servers_used = 0
        output = []
        for cache_id, cache in self.cache_servers.items():
            if cache.free_space == cache.total_capacity:
                # server was not used at all
                continue

            servers_used += 1
            line = [cache_id]
            for v in cache.videos_stored_ids:
                line.append(v)
            output.append(line)

        with open('%s.out' % self.savings, 'w') as fo:
            fo.write("%s\n" % servers_used)
            for videos in output:
                fo.write("%s\n" % ' '.join([str(v) for v in videos]))
