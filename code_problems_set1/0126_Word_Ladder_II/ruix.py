from typing import List

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        ans = []    # store the shortest paths here!
        if endWord not in wordList:
            return ans

        # use this dictionary to store the shortest path from beginWord to each word in wordList.
        word_to_path = {}
        for word in wordList:
            word_to_path[word] = []
        word_to_path[beginWord] = [[beginWord]]
        
        # use this set of store the words that I've seen in higher layers.
        seen = set()
        seen.add(beginWord)
        
        found = False       # use this flag to check if I've found end word.
        queue = [beginWord] # use this array as a queue on all tree nodes on current layer.
        while not found and len(queue):
            temp = []        # use this array to store the tree nodes I woud traverse in next layer.
            new_seen = set() # use this set to store the tree nodes that I've seen in current layer.
            for currentWord in queue:
                for word in wordList:
                    # if I've seen this word in higher layers, then this path cannot be the shortest
                    # path.
                    if word in seen:
                        continue
                    # only proceed if this word is different in only one char with previous word.
                    if self.diifer_by_one(currentWord, word):
                        new_seen.add(word)  # I would add this word as have seen in this layer.
                        # add the path to dictionary.
                        for path in word_to_path[currentWord]:
                            word_to_path[word].append(path + [word])
                        if word == endWord:
                            # in this case I've found the end word, no need to proceed to next layer.
                            found = True
                        else:
                            temp.append(word)  
                # delete in case future contradition, no need any way.
                word_to_path[currentWord] = []
            # before proceeding to next layer, set the seen set.
            for ele in new_seen:
                seen.add(ele)
            queue = temp          

        return word_to_path[endWord]
            
    
    def diifer_by_one(self, s1: str, s2: str) -> bool:
        d = 0

        for i in range(len(s1)):
            if s1[i] != s2[i]:
                d += 1
                if d >= 2:
                    return False

        return d