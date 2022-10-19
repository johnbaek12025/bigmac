def rotate(nums, k):
    if len(nums) < k:
        k = k - len(nums)
    temp = nums[:len(nums) - k]
    nums[:len(nums) - k] = nums[len(nums) - k:]
    nums[len(nums) - k:] = temp[:]
    print(nums)



nums = [1,2,3]
k = 4
rotate(nums, k)