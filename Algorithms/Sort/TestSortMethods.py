import unittest
import random as rd
import Sort

class TestSortMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.all_arrays = []
        # take 100 arrays with lengths in [50, 99]
        for _ in range(100):
            # each number could be rd.randint(-1e3, 1e3) if not testing radix sort.
            self.all_arrays.append([rd.randint(0, 1e3) for __ in range(rd.randint(50, 100))])
        # store a sorted copy of each of the arrays.
        self.all_sorted_arrays = [sorted(lst) for lst in self.all_arrays]
        
        self.sorter = Sort.Sort()

        return super().setUp()
    
    def test_bubble_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.bubble_sort(lst))
    
    def test_selection_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.selection_sort(lst))
    
    def test_insertion_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.insertion_sort(lst))
    
    def test_shell_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.shell_sort(lst))
    
    def test_quick_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.quick_sort(lst))
    
    def test_merge_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.merge_sort(lst))
    
    def test_heap_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.heap_sort(lst))
    
    def test_radix_sort(self):
        for i in range(100):
            lst = self.all_arrays[i].copy()
            self.assertEqual(self.all_sorted_arrays[i], self.sorter.radix_sort(lst))

if __name__ == '__main__':
    unittest.main()