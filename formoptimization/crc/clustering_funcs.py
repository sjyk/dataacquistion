from clustering_tree import Tree
from R_to_V import get_bag_of_words
from spectral_clustering import *
import random
import math
import IPython


def cluster_spectral_k_means(groups,threshold=lambda x:x<=0,num_groups=lambda x:int(math.ceil(len(x)/4.0)),num_dims=2,opt_cutoff=.5):
	word_dict={}
	for group in groups:
		# if isinstance(group.item,list):
		# 	words=group.item
		# else:
		words=get_bag_of_words(','.join(group.item))
		# group.item=' '.join(group.item)
		for word in words:
			if word=='1':
				print word
			word_dict[word]=1
	word_list=word_dict.keys()

	similarity_mat=map_blocks_similarity(groups,word_list)
	filtered_mat=filter_edges(similarity_mat,threshold)
	W=map_edges_tree(filtered_mat,groups)[1]
	laplacian=get_laplacian(W)
	eigen=calc_eigen(laplacian,num_dims)
	list_of_points=map(lambda x:Point(x[1].tolist(),groups[x[0]]),enumerate(eigen))
	print len(groups),' ',len(groups)/4.0, ' ',math.ceil(len(groups)/4.0),' ',int(math.ceil(len(groups)/4.0)),' ',num_groups(groups) 


	clusters=map(lambda x:map(lambda y:y.block,x.points),kmeans(list_of_points,num_groups(groups),opt_cutoff))
	return clusters



class Point:
    '''
    An point in n dimensional space
    '''
    def __init__(self, coords,block=None):
        '''
        coords - A list of values, one per dimension
        '''
        
        self.coords = coords
        self.n = len(coords)
        self.block=block
        
    def __repr__(self):
        return str(self.coords)

class Cluster:
    '''
    A set of points and their centroid
    '''
    
    def __init__(self, points):
        '''
        points - A list of point objects
        '''
        
        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        # The points that belong to this cluster
        self.points = points
        
        # The dimensionality of the points in this cluster
        self.n = points[0].n
        
        # Assert that all points are of the same dimensionality
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: wrong dimensions")
            
        # Set up the initial centroid (this is usually based off one point)
        self.centroid = self.calculateCentroid()
        
    def __repr__(self):
        '''
        String representation of this object
        '''
        return str(self.points)
    
    def update(self, points):
        '''
        Returns the distance between the previous centroid and the new after
        recalculating and storing the new centroid.
        '''
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid,self) 
        return shift
    
    def calculateCentroid(self):
        '''
        Finds a virtual center point for a group of n-dimensional points
        '''
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]
        
        return Point(centroid_coords)

def kmeans(points, k, cutoff):
    
    # Pick out k random points to use as our initial centroids
    initial = random.sample(points, k)
    
    # Create k clusters using those centroids
    clusters = [Cluster([p]) for p in initial]
    # print points
    # print '\n'
    # print clusters
    # print '\n'
    # print k
    
    # Loop through the dataset until the clusters stabilize
    loopCounter = 0
    while True:
        # Create a list of lists to hold the points in each cluster
        lists = [ [] for c in clusters]
        clusterCount = len(clusters)
        
        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
            # Get the distance between that point and the centroid of the first
            # cluster.
            if clusterCount==0:
            	IPython.embed()
            smallest_distance = getDistance(p, clusters[0].centroid)

        
            # Set the cluster this point belongs to
            clusterIndex = 0
        
            # For the remainder of the clusters ...
            for i in range(clusterCount - 1):
                # calculate the distance of that point to each other cluster's
                # centroid.
                distance = getDistance(p, clusters[i+1].centroid)
                # If it's closer to that cluster's centroid update what we
                # think the smallest distance is, and set the point to belong
                # to that cluster
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            lists[clusterIndex].append(p)
        
        # Set our biggest_shift to zero for this iteration
        biggest_shift = 0.0
        
        # As many times as there are clusters ...
        for i in range(clusterCount):
            # Calculate how far the centroid moved in this iteration
            shift = clusters[i].update(lists[i])
            # Keep track of the largest move from all cluster centroid updates
            biggest_shift = max(biggest_shift, shift)
        
        # If the centroids have stopped moving much, say we're done!
        if biggest_shift < cutoff:
            print "Converged after %s iterations" % loopCounter
            break
    return clusters

def getDistance(a, b,cluster1=None):
    '''
    Euclidean distance between two n-dimensional points.
    Note: This can be very slow and does not scale well
    '''
    if a.n != b.n:
    	print a.n,' ',b.n
    	print cluster1.points
        raise Exception("ILLEGAL: non comparable points")
    
    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
    return math.sqrt(ret)



