from solution import Solution

from logic import add_random_video, remove_empty_endpoints


if __name__ == '__main__':
    # init
    fd = open('me_at_the_retirement_home.in')
    solution = Solution(fd)

    # apply logic
    remove_empty_endpoints(solution)
    add_random_video(solution)

    # give back results
    solution.dump()
