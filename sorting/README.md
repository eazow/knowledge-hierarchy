### 排序算法

##### 1. 快速排序
quick_sort.py

以第一个数为基准，比该数小的数放在该数左边，比该数大的数放在该数右边，然后递归调用

##### 2. 选择排序
selection_sort.py

每次选择出最小的元素，依次放入位置1、2、3...


##### 3. 堆排序

- 将无需序列构建成一个堆，根据升序降序需求选择大顶堆或小顶堆;
- 将堆顶元素与末尾元素交换，将最大元素"沉"到数组末端;
- 重新调整结构，使其满足堆定义，然后继续交换堆顶元素与当前末尾元素，反复执行调整+交换步骤，直到整个序列有序。
