import numpy as np
import pprint
import random
import time
def read_google(filename):
    data = dict()


    with open(filename, "r") as fin:

        system_desc = next(fin)
        number_of_videos, number_of_endpoints, number_of_requests, number_of_caches, cache_size = system_desc.split(" ")
        number_of_videos = int(number_of_videos)
        number_of_endpoints = int(number_of_endpoints)
        number_of_requests = int(number_of_requests)
        number_of_caches = int(number_of_caches)
        cache_size = int(cache_size)
        video_ed_request = dict()
        video_size_desc = next(fin).strip().split(" ")
        
        ed_cache_list = []

        # ## CACHE SECTION

        ep_to_cache_latency = [] 

        ep_to_dc_latency = [] 
        for i in range(number_of_endpoints):

            ep_to_dc_latency.append([])
            ep_to_cache_latency.append([])

            dc_latency, number_of_cache_i = next(fin).strip().split(" ")
            dc_latency = int(dc_latency)
            number_of_cache_i = int(number_of_cache_i)

            ep_to_dc_latency[i] = dc_latency

            for j in range(number_of_caches):
                ep_to_cache_latency[i].append(ep_to_dc_latency[i])

            cache_list = []
            for j in range(number_of_cache_i):
                cache_id, latency = next(fin).strip().split(" ")
                cache_id = int(cache_id)
                cache_list.append(cache_id)
                latency = int(latency)
                ep_to_cache_latency[i][cache_id] = latency

            ed_cache_list.append(cache_list)

        # ## REQUEST SECTION
        for i in range(number_of_requests):
            video_id, ed_id, requests = next(fin).strip().split(" ")
            video_ed_request[(video_id, ed_id)] = requests

    data["number_of_videos"] = number_of_videos
    data["number_of_endpoints"] = number_of_endpoints
    data["number_of_requests"] = number_of_requests
    data["number_of_caches"] = number_of_caches 
    data["cache_size"] = cache_size
    data["video_size_desc"] = video_size_desc
    data["ep_to_dc_latency"] = ep_to_dc_latency
    data["ep_to_cache_latency"] = ep_to_cache_latency
    data["ed_cache_list"] = ed_cache_list
    data["video_ed_request"] = video_ed_request

    return data

data = read_google("me_at_the_retirement_home.in")
for key in data:
    print(key, data[key])


# The below 2d arrays can be useful for plugging into the viable check or hill climbing functions
    # An initial "default" solution of all zeros. 
start_solution = np.zeros((data["number_of_caches"], data["number_of_videos"]), dtype=np.int)
    # An initial random solution of random 1s or 0s. 
random_solution = np.random.randint(2, size=(data["number_of_caches"], data["number_of_videos"]))

    # Solution provided in google slides, useful for checking the score function
new_soluton = np.array([[0, 0, 1, 0, 0],
               [0, 1, 0, 1, 0],
               [1, 1, 0, 0, 0]], np.int)

    #Mostly a solution just for hill climbing to show that a valid starting solution which is not already at a local maximum 
    #will start to go through the hill climbing process 
sub_soluton = np.array([[0, 0, 1, 0, 0],
               [0, 1, 0, 1, 0],
               [1, 0, 0, 0, 0]], np.int)

def viable_check(start_solution):
# look into the solution assuming that it is viable
    viable = True
    for i in range(0, (data["number_of_caches"])):
        sumsize = 0
        for j in range(0, (data["number_of_videos"])):
            # check if the given position in a solution is 1, if so then add the file size to a counter
            if start_solution[i][j] == 1:
                sumsize += int(data["video_size_desc"][j])
        # check if the total value of the counter is now greater than the standard cache size
        if sumsize > data["cache_size"]:
            viable = False
            return viable
    return viable

#by far the hardest part of the assignment was the score function 
def score(graph):
    Total = 0
    Final=0
    if viable_check(graph):
        for key in data["video_ed_request"]:
            #manipulating dictionaries to get the information needed
            video = int(key[0])
            endpoint = int(key[1])
            ChacheList = []
                    
            for i in range(len(graph)): 
    
                if graph[i][video] == 1:
                    ChacheList += i,
    
            BestLat = data["ep_to_dc_latency"][endpoint]
            
            # Get the best latency for any given endpoint
            for b in ChacheList:
                BestLat = min(BestLat, data["ep_to_cache_latency"][endpoint][b])
            
            # calculate the score 
            score = (int(data["ep_to_dc_latency"][endpoint]) - BestLat) * int(data["video_ed_request"][key])
            Total += score
        
        # sum the number of requests for each video, convert score into formula provided by google 
        Totalreq = 0     
        for i in data["video_ed_request"]:
            Totalreq += int(data["video_ed_request"][i])
        Final = int((Total * 1000) / Totalreq)
    return Final

#the story of one solution's struggle to climb hills and improve itself on a journey of discovery  
def hill(new_soluton):
    first_score = 0
    max_score = score(new_soluton)
    Max_sol = np.array(new_soluton)
    print("Entering hill climbing process")
    #here there could be another solution with the same score but that is the problem with a local maximum
    while max_score != first_score:
        print("Entering loop with : ", Max_sol)
        print("Score is : ", max_score)
        print()
        first_score = max_score

        for a in range(len(new_soluton)):
            for b in range(len(new_soluton[a])):        
                secondsol = np.array(Max_sol)
                secondsol[a][b] ^= 1

                if viable_check(secondsol):
                    if score(secondsol) > max_score:
                        max_score = score(secondsol)
                        Max_sol = np.array(secondsol)

    print("max score is: ", max_score, "\nThat comes from solution: \n", Max_sol)
    #it can't get any better than this, queue the music from the Rocky films
    return Max_sol

def genetic(num_gen):
    
    #placeholder solution that is going to be used to become a child 
    new_soluton = np.zeros((data["number_of_caches"], data["number_of_videos"]), dtype=np.int)
    
    #use population function to generate random population
    sol_array = population()    
    
    #placeholder max values
    max_score=0
    max_sol=sol_array[0]
    
    #this is the length the population should revert to when children are added
    desired_pop=len(sol_array)
    
    generation_count=1
    while generation_count<num_gen:
        generation_count+=1
        #implement sorting function to distinguish the best from the rest
        #(current implementation of the function unfortunately removes duplicate scoring solutions)
        sol_array=sorting(sol_array)
        
        #check if there is a new, highest scoring solution in the population. if so then set it as the max
        current_max = score(sol_array[0])
        if current_max>max_score:
            max_score=current_max
            max_sol=sol_array[0]
        
        #filter down the population, the weak will perish!     
        survival_chance = round(len(sol_array) * 0.5)
        sol_array = sol_array[:survival_chance]
        
        #each solution left has a chance at mutation. Will we make the incredible hulk? 
        sol_array=mutant_chance(sol_array)
        
        child = []
        counter_child = 0
        growth_room = desired_pop-len(sol_array)
        #process of making babies! Not sure how to make it more romantic. candle light and dinner might be good here
        while counter_child < growth_room:
            
            #pick which two parents are going to get together 
            first_index = random.randint(0, len(sol_array) - 1)
            second_index = random.randint(0, len(sol_array) - 1)
            
            # make sure none are allowed to fancy/clone themselves. If they try then pick another lucky couple
            if first_index != second_index:
                     
                #and the couple are. . . 
                first_parent = sol_array[first_index]
                second_parent = sol_array[second_index]
        
                #using placeholder array as the embryo to build from
                Child_sol = np.array(new_soluton)
                for a in range(len(new_soluton)):
                    for b in range(len(new_soluton[a])):
                        
                        #Look away for this section, adults eyes only
                        # randomly select a parent to take the corresponding trait from
                        parent_select = random.randint(0, 1)
                        if parent_select == 0:
                            Child_sol[a][b] = first_parent[a][b]
                        else:
                            Child_sol[a][b] = second_parent[a][b]
                
                #if the child is viable keep, otherwise throw away and go again. (don't do that in real life)
                if viable_check(Child_sol):
                    #congratulations! it is a . . . solution
                    child.append(Child_sol)
                    counter_child += 1
        
        #children grow up so fast! Time for them to join the wider population
        sol_array.extend(child)
    print("after",generation_count,"generations","max score",max_score,"from:\n",max_sol)
    return max_sol
def population():
    sol_array = []
    counter = 0
    #need to determine how large to set the population. for now I use arbitrary thresholds of the number of caches 
    if data["number_of_caches"]<10: 
        pop_size = 50
    elif data["number_of_caches"]<20:
        pop_size = 100
    else:
        pop_size = 150
    while counter < pop_size:
        parent = np.random.randint(2, size=(data["number_of_caches"], data["number_of_videos"]))
        if viable_check(parent):
            sol_array.append(parent)
            counter += 1
    return sol_array

#takes as input an array of solutions 
def sorting(pop):
    
    #use a dictionary that will take the combination of scores and solutions
    seg = {}
    #generate they key for the dictionary
    for i in range(len(pop)):
        seg[score(pop[i]),i] = (pop[i])
        
    #sort in descending order of the scores
    keys = sorted(seg.keys())[::-1]
    
    #new ordered population
    solution = [seg[key] for key in keys]
    #one potential big problem here is that the new solution won't keep duplicate solutions. 
    #this means there is a risk the ordered solutions will be very few and that any explicit filtering later would
    #reduce the population too much 
    
    return solution

def random_search(Seconds):
    max_score =0
    max_solution = np.zeros((data["number_of_caches"], data["number_of_videos"]), dtype=np.int)
    start_time = time.time()
    while ((time.time() - start_time)<Seconds):
        random_solution = np.random.randint(2, size=(data["number_of_caches"], data["number_of_videos"]))
        if viable_check(random_solution):
            random_score = score(random_solution)
            if random_score > max_score:
                max_score=random_score
                max_solution=random_solution
    print("Random search:",max_solution,max_score)
    return max_solution

def mutant_chance(sol_array):
    #mutation segment
    
    #every solution has a chance of mutation
    for i in sol_array:

        #set the chance to be 1 divided by twice the product of caches by videos.seemed to keep mutations low enough 
        if random.random()<(1/((data["number_of_caches"]* data["number_of_videos"])*2)):
            #randomly set the position to be changed
            first=random.randint(0, (len(i)-1))
            second =random.randint(0, (len(i[first])-1))
        
            i[first][second]^= 1
            #Hulk smash!
        
            
    #One issue to note is that this will result in unviable solutions being created. However their score will be 0.        
    return sol_array
        
        
#Followed the guide on http://katrinaeg.com/simulated-annealing.html
#temperamental when using, often it only finds solutions that are zero. When it works it tends to work very well, often getting
#high scores. I suspect I need to improve my acceptance_probability function 
def simulated_annealing():
    
    #creating starting solution and score
    random_solution = np.random.randint(2, size=(data["number_of_caches"], data["number_of_videos"]))
    random_score = score(random_solution)
    
    #variables for the simulated annealing process 
    temprature = 1.0
    temprature_min = 0.0001
    alpha=0.9
    
    #start the simulated annealing process 
    while temprature>temprature_min:
        
        i=1
        while i <= 1000:
            #creating a neighbouring solution to the original 
            random_neighbour=np.array(random_solution)
            #random positions selected to create new neighbour
            first=random.randint(0, len(random_neighbour) - 1)
            second =random.randint(0, len(random_neighbour) - 1)
            #neighbour created
            
            random_neighbour[first][second]^=1
            neighbour_score = score(random_neighbour)
            
            #comparing the new solution to the original and calculate the acceptance_probability 
            #want it to always be above 1 if the new solution is better than the old and between 0 and 1 if not
            if neighbour_score>random_score:
                    acceptance_probability=1
            else:
                    acceptance_probability=((neighbour_score+1)/(random_score+1))/(temprature)
                    #print(acceptance_probability)
            
            if random.random() < acceptance_probability:
                random_solution=random_neighbour
                random_score=neighbour_score

            i+=1
        
    
        temprature*=alpha
    print(random_score)
    return random_solution


#print(viable_check(start_solution))
#print(score(new_soluton))
#hill(sub_soluton)
#genetic(50)
#print(population())
#print(sorting(population()))
#print(mutant_chance(population()))
#random_search(30)
#simulated_annealing()
hill(random_search(30))