
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(len(nums)):
                if j != i:
                    if nums[i] + nums[j] == target:
                        return [i, j]

def main():
  sol = Solution()
  sol.twoSum(nums=[], target=10)

if __name__ == "__main__":
  main()
