class Solution:
    def longestPalindrome(self, s: str) -> str:
        # base case: if s is of length <= 1, then itself is palindrome.
        if len(s) <= 1:
            return s

        # s1 is s with a '|' inserted before every single character, and add one more '|' at the end.
        # use s1 because we need to consider about palindrome of even length as well.
        s1 = '|'
        for i in range(len(s)):
            s1 += s[i] + '|'
        # this is an array recording largest radius of palindrome centering at index i in s1.
        longest_radius = [0] * len(s1)

        center, radius = 0, 0
        while center < len(s1):
            # find the radius of longest palindrome centering at current center.
            while (center-radius-1) >= 0 and (center+radius+1) < len(s1):
                if s1[center-radius-1] != s1[center+radius+1]:
                    break
                radius += 1
            longest_radius[center] = radius

            # use the information we get for center to go further.
            old_center, old_radius = center, radius
            center, radius = center + 1, 0
            # utilize the fact that each substring centering at the center of a palindrome is itself
            # a palindrome as well.
            while center <= old_center+old_radius:
                mirrored_center = old_center - (center-old_center)  # the mirrored position of center.
                # max_mirrored_rad is the distance between center and the boundary of longest palindrome
                # centering at the old center.
                max_mirrored_rad = (old_center+old_radius) - center

                if longest_radius[mirrored_center] < max_mirrored_rad:
                    # in this case apparently the longest radius of palindrome centering at the center
                    # is same as mirrored_center.
                    longest_radius[center] = longest_radius[mirrored_center]
                    center += 1
                elif longest_radius[mirrored_center] > max_mirrored_rad:
                    # in this case, apparently the longest radius of palindrome centering at the center
                    # is max_mirrored_rad as s1[old_center + old_radius + 1] != s1[old_center - old_ra-
                    # dius - 1] but s1[mirrored_center - max_mirrored_rad - 1] = s1[mirrored_center + 
                    # max_mirrored_rad + 1] = s1[center - max_mirrored_rad - 1] != s1[center + max_mir-
                    # rored_rad + 1].
                    longest_radius[center] = max_mirrored_rad
                    center += 1
                else:
                    # in this case, it is possible that the longest radius of palindrome centering at the
                    # center is longer, so set the radius to be max_mirrored_rad and proceed to the next
                    # iteration.
                    radius = max_mirrored_rad
                    break
        
        max_center = max([i for i in range(len(s1))], key=lambda i: longest_radius[i])
        max_radius = longest_radius[max_center] // 2    # find the radius in original s.
        if max_center % 2:
            # in this case, the longest palindrome is of odd length.
            return s[max_center//2 - max_radius:max_center//2 + max_radius + 1]
        else:
            # in this case, the longest palindrome is of even length.
            return s[max_center//2 - max_radius:max_center//2 + max_radius]    