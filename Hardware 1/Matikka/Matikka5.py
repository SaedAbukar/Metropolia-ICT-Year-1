{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "initial_id",
   "metadata": {
    "collapsed": true,
    "ExecuteTime": {
     "end_time": "2024-02-28T12:58:16.049536100Z",
     "start_time": "2024-02-28T12:58:15.938433900Z"
    }
   },
   "outputs": [],
   "source": [
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Matrix 1:\n",
      "[[-1  2]\n",
      " [ 3  1]]\n",
      "\n",
      "Matrix 2:\n",
      "[[ 0  1  3]\n",
      " [ 2 -3  5]]\n",
      "\n",
      "Result of matrix multiplication:\n",
      "[[ 4 -7  7]\n",
      " [ 2  0 14]]\n"
     ]
    }
   ],
   "source": [
    "# Define matrices\n",
    "oneA = np.array([[-1, 2],\n",
    "                    [3, 1]])\n",
    "\n",
    "oneA_two = np.array([[0, 1, 3],\n",
    "                    [2, -3, 5]])\n",
    "\n",
    "# Perform matrix multiplication\n",
    "result = np.dot(oneA, oneA_two)\n",
    "\n",
    "print(\"Matrix 1:\")\n",
    "print(oneA)\n",
    "print(\"\\nMatrix 2:\")\n",
    "print(oneA_two)\n",
    "print(\"\\nResult of matrix multiplication:\")\n",
    "print(result)\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2024-02-28T12:58:16.059201200Z",
     "start_time": "2024-02-28T12:58:16.055602400Z"
    }
   },
   "id": "ed183aba8d350ef8"
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Matrix 1:\n",
      "[[ 1  3  5]\n",
      " [ 0 -2  1]\n",
      " [ 2 -1  4]]\n",
      "\n",
      "Matrix 2:\n",
      "[[ 1]\n",
      " [-3]\n",
      " [-1]]\n",
      "\n",
      "Result of matrix multiplication:\n",
      "[[ 4 -7  7]\n",
      " [ 2  0 14]]\n"
     ]
    }
   ],
   "source": [
    "oneB = np.array([[1, 3, 5],\n",
    "                [0, -2, 1],\n",
    "                [2, -1, 4]])\n",
    "\n",
    "oneB_two = np.array([[1],\n",
    "                    [-3],\n",
    "                    [-1]])\n",
    "\n",
    "# Perform matrix multiplication\n",
    "result = np.dot(oneA, oneA_two)\n",
    "\n",
    "print(\"Matrix 1:\")\n",
    "print(oneB)\n",
    "print(\"\\nMatrix 2:\")\n",
    "print(oneB_two)\n",
    "print(\"\\nResult of matrix multiplication:\")\n",
    "print(result)\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2024-02-28T12:58:16.065906600Z",
     "start_time": "2024-02-28T12:58:16.059201200Z"
    }
   },
   "id": "e552b4b65ce78746"
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Matrix 1:\n",
      "[[ 2  0  1]\n",
      " [ 1 -3  4]\n",
      " [ 0  1  5]]\n",
      "\n",
      "Matrix 2:\n",
      "[[ 3]\n",
      " [-5]\n",
      " [ 7]]\n",
      "\n",
      "Result of matrix multiplication:\n",
      "[[ 4 -7  7]\n",
      " [ 2  0 14]]\n"
     ]
    }
   ],
   "source": [
    "oneC = np.array([[2, 0, 1],\n",
    "                [1, -3, 4],\n",
    "                [0, 1, 5]])\n",
    "\n",
    "oneC_two = np.array([[3],\n",
    "                    [-5],\n",
    "                    [7]])\n",
    "\n",
    "# Perform matrix multiplication\n",
    "result = np.dot(oneA, oneA_two)\n",
    "\n",
    "print(\"Matrix 1:\")\n",
    "print(oneC)\n",
    "print(\"\\nMatrix 2:\")\n",
    "print(oneC_two)\n",
    "print(\"\\nResult of matrix multiplication:\")\n",
    "print(result)\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2024-02-28T12:58:16.072068300Z",
     "start_time": "2024-02-28T12:58:16.065906600Z"
    }
   },
   "id": "a625706e254a3d94"
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Matrix 1:\n",
      "[[ 1 -4  2]\n",
      " [ 3  0 -2]\n",
      " [ 2  1  0]]\n",
      "\n",
      "Matrix 2:\n",
      "[[ 5  1 -1]\n",
      " [-2  1  3]\n",
      " [ 0  3  4]]\n",
      "\n",
      "Result of matrix multiplication:\n",
      "[[ 4 -7  7]\n",
      " [ 2  0 14]]\n"
     ]
    }
   ],
   "source": [
    "oneD = np.array([[1, -4, 2],\n",
    "                [3, 0, -2],\n",
    "                [2, 1, 0]])\n",
    "\n",
    "oneD_two = np.array([[5, 1, -1],\n",
    "                    [-2, 1, 3],\n",
    "                    [0, 3, 4]])\n",
    "\n",
    "# Perform matrix multiplication\n",
    "result = np.dot(oneA, oneA_two)\n",
    "\n",
    "print(\"Matrix 1:\")\n",
    "print(oneD)\n",
    "print(\"\\nMatrix 2:\")\n",
    "print(oneD_two)\n",
    "print(\"\\nResult of matrix multiplication:\")\n",
    "print(result)\n"
   ],
   "metadata": {
    "collapsed": false,
    "ExecuteTime": {
     "end_time": "2024-02-28T12:58:16.078423600Z",
     "start_time": "2024-02-28T12:58:16.072068300Z"
    }
   },
   "id": "fc73dbb3edb4a060"
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
