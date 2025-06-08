from ..general import MinHeap as heap
#import .general.MinHeap as heap

import json
import os

'''
This is a prototype of a Directed Graph object designed to be swift at the expense of space.

Ideally, this class would be used to compute directed graphs where the verticies are strings,
the result is then either periodically compressed or serialized to a compressed form, where it can 
be used further as an immutable Directed Graph
'''
class DirectedKeyGraph:

    serialize_fields = ["vertex_list", "edge_list"]

    @classmethod
    def loadJsonFormat(cls, obj_str):
        if not isinstance(obj_str, str) or len(obj_str) <= 0:
            raise TypeError(f"expected obj_str to be a string, but got: {type(obj_str)}")
        if os.path.isfile(obj_str):
            if obj_str.split(".")[-1] == 'json':
                json_obj = json.load(obj_str)
            else:
                raise IOError(f"Can not open file. Expected json file, but got {obj_str.split('.')[-1]}")
        else:
            json_obj = json.loads(obj_str)
        return_list = []
        for field in cls.serialize_fields:
            return_list = json_obj.get(field, [])
        return return_list[:]

    supported_serialize_formats = {
        'json': loadJsonFormat
    }
        

    def __str__(self):
        cur = ""
        cur += "\t----- Verticies -----\n"
        for i in range(len(self.V)):
            cur += f"{i}:\t{str(self.V[i])}\n"
        cur += "\n\n"
        cur += "\t----- Edges ------\n"
        for i in range(len(self.E)):
            cur += f"{i}:\t{str(self.E[i])}\n"
        return cur

    def __repr__(self):
        cur = self.__str__()
        cur += "\n\n"
        cur += "\t----- Back Edges ------\n"
        for i in range(len(self.backE)):
            cur += f"{i}:\t{str(self.backE[i])}\n"
        return cur

    '''
    Constructor method that produces a blank Graph.
    '''
    def __init__(self):
        self.vMap = {} # Dictionary representing map from value -> index
        self.unusedV = heap() # priority queue of next unused Index, empty if number vertex == len(self.V)
        self.V = [] # Array representing map from index -> value
        self.E = [] # Adjacency List for edge representation
        self.backE = [] # BackEdges for Adjacency List

    '''
    Internal function that converts the string represetion to an internal representation that 
    requires less memory.

    @param  {String}    vertex  The string representation to convert.

    @return {Integer}       The integer representing the string representation.
    @error  {ValueError}    Raises an error if there is an issue with internal representation structures.
    '''
    def __vertexToInternal(self, vertex):
        if isinstance(vertex, int) and vertex >= 0 and vertex < len(self.V):
            if self.V[vertex] == None:
                raise ValueError(f"{type(vertex)}: {vertex} is an empty internal index")
            else:
                return vertex
        elif isinstance(vertex, str) and self.vExists(vertex):
            return self.vMap[vertex]
        else:
            raise ValueError(f"{type(vertex)}: {vertex} is not in Graph")

    '''
    Internal function that coverts a set of string representation to a set of internal representations
    that require less memory. The vSet parameter should be list, set or tuple. 
    Further collections could be added in the future.

    @param  {Collection}    vSet    The collection representing a set of string representations.
    
    @return {Collection}        A collection (same type as vSet) representing a set of integer representations.
    @error  {ValueError}        Raises an error if there is a problem with the internal representation structures.
    @error  {TypeError}         The vSet Collection is not a recognized type.
    '''
    def __vSetToInternal(self, vSet):
        try:
            lis = []
            for v in vSet:
                try:
                    lis.append(self.__vertexToInternal(v))
                except:
                    continue
            if isinstance(vSet, list):
                return lis
            elif isinstance(vSet, set):
                return set(lis)
            elif isinstance(vSet, tuple):
                return tuple(lis)
            else:
                raise TypeError(f"{type(vSet)} is iterable but unrecognized type")
        except:
            raise

    '''
    An Alias for __vSetToInternal function. Additionally, there is a check to ensure that the given collection
    and the returned collection is of the same length. As with the __vSetToInternal function, the parameter is 
    expected to be a list, set or tuple. 
    Further collections could be added in the future.

    Note:
        The first two elements (e_1, e_1) in the collection represent the directed graph edge from e_1 to e_2

    @param  {Collection}    edge    A collection representing the information of an Edge in the graph.

    @return {Collection}        A collection of the same type representing the information as integers.
    @error  {ValueError}        Raises an error if there is a problem with the internal representation structures.
    @error  {TypeError}         The vSet Collection is not a recognized type.
    '''
    def __edgeToInternal(self, edge):
        try:
            internalTuple = self.__vSetToInternal(edge)
            if len(edge) == len(internalTuple):
                return internalTuple
            else:
                raise ValueError(f"Dimension Incompatibility:\n\tEdge: {len(edge)}\n\tInternal: {len(internalTuple)}")
        except:
            raise

    '''
    Checks if a given vector exists.

    @param  {String}   vertex   The string represention of a vertex to test.

    @return {Boolean}       True if the vertex exists in the internal structure of the Graph, False otherwise.
    '''
    def vExists(self, vertex):
        try:
            return vertex == self.V[self.vMap[vertex]]
        except:
            return False

    '''
    Checks if an edge exists. To be used internally by edgeExists function.
    Currently, an Edge is defined as a tuple of the form (vertex_1, vertex_2)
    to represent an edge from vertex_1 to vertex_2
    
    Note:
        There are no weights at the moment to keep it simple.

    @param  {Collection}    edge            A collection representing an Edge, recommended to be Tuple
    @param  {Collection}    edgeCollection  The internal data structure used to store Edges.
    @param  {Boolean}       conversion      [Optional] Represents if conversion from string to int is required.

    @return {Boolean}       True if the edge exists in the given collection, False otherwise.
    '''
    def eExists(self, edge, edgeCollection, conversion=True):
        if conversion:
            indexTuple = self.__edgeToInternal(edge)
        else:
            indexTuple = edge
        for e in edgeCollection[indexTuple[0]]:
            if e == indexTuple[1:]:
                return True
            else:
                continue
        return False

    '''
    Checks if an edge exists. To be used internally by edgeExists function.
    Currently, an Edge is defined as a tuple of the form (vertex_1, vertex_2)
    to represent an edge from vertex_1 to vertex_2.

    Alias of the eExists function with the Edge list data structure collection.
    
    Note:
        There are no weights at the moment to keep it simple.

    @param  {Collection}    edge        A collection representing an Edge, recommended to be Tuple
    @param  {Boolean}       conversion  [Optional] Represents if conversion from string to int is required.

    @return {Boolean}       True if the edge exists in the edge List, False otherwise.
    '''
    def edgeExists(self, edge, conversion=True):
        return self.eExists(edge, self.E, conversion)

    '''
    Static method for reversing an edge represention. 
    From (v_1, v_2) to (v_2, v_1), so an edge from v_1 vertex to v_2 vertex 
    would be changed to be an edge from v_2 vertex to v_1 vertex.

    Note:
        This is useful from calculating back edges for various further computations.

    @param  {Collection}    edge    The representation of edge between two verticies

    @return {Collection}        The reversed edge.
    '''
    @staticmethod
    def reverseEdge(edge):
        second = edge[0]
        first = edge[1]
        backEdge = (first, second)
        if len(edge) > len(backEdge):
            backEdge = backEdge + edge[2:]
        return backEdge

    '''
    Add a Vertex to Graph.

    Note:
        If the vertex already exists, it counts as not being able to be added and returns False.

    @param  {String}    vertex  The string representation of a vertex.

    @return {Boolean}       True if the vertex can be added, False otherwise.
    '''
    def addVertex(self, vertex):
        if self.vExists(vertex):
            return False # Already exists
        elif self.unusedV.size() > 0:
            _, nextIndex = self.unusedV.next()
            self.V[nextIndex] = vertex
            self.vMap[vertex] = nextIndex
            self.E[nextIndex] = set()
            self.backE[nextIndex] = set()
        else:
            self.vMap[vertex] = len(self.V)
            self.V.append(vertex)
            self.E.append(set())
            self.backE.append(set())
        return self.vExists(vertex)
        
    '''
    Removes a vertex from the graph, including all edges from and to the given vertex.

    Note:
        If the vertex does not exist in the graph, this function returns False.

    @param  {String}    vertex  A string representation of a vertex.

    @return {Boolean}           True if the vertex was removed, False otherwise or a ValueError encountered.
    @error  {ReferenceError}    Raises if the was an issue remvoing an Edge associated with this vertex.
    '''
    def removeVertex(self, vertex):
        try:
            rmIndex = self.__vertexToInternal(vertex)
            for e in self.E[rmIndex]:
                if self.__removeE((e[0], rmIndex), self.backE):
                    continue
                else:
                    raise ReferenceError(f"Unable to remove Edge: {e}")
            self.E[rmIndex] = None
            for e in self.backE[rmIndex]:
                if self.__removeE(self.__class__.reverseEdge(e), self.E):
                    continue
                else:
                    raise ReferenceError(f"Unable to remove Edge: {e}")
            self.backE[rmIndex] = None # remove all copies of backedges
            self.V[rmIndex] = None
            self.unusedV.add(rmIndex, rmIndex) # Makes the index be the weight so it fills lower indecies first
            del self.vMap[vertex]
            return not self.vExists(vertex)
        except ValueError as e:
            return False # no internal representation exists, so vertex could not be removed

    '''
    Internal function for adding an edge to an internal edge collection.

    @param  {Collection}    edge            A representation of edge.
    @param  {Collection}    edgeCollection  The internal data structure representing an edge list.

    @return {Boolean}       True if the edge was added, False otherwise.
    @error  {TypeError}     Raise if internal data structure could not add the edge.
    '''
    def __addE(self, edge, edgeCollection):
        try:
            indexTuple = self.__edgeToInternal(edge)
            for e in edgeCollection[indexTuple[0]]:
                if e == indexTuple[1:]:
                    return False # Edge Already exists
                else:
                    continue
            if hasattr(edgeCollection[indexTuple[0]], 'append'):
                edgeCollection[indexTuple[0]].append(indexTuple[1:])
            elif hasattr(edgeCollection[indexTuple[0]], 'add'):
                edgeCollection[indexTuple[0]].add(indexTuple[1:])
            else:
                raise TypeError(f"Unable to append/add to collection of type {type(edgeCollection[indexTuple[0]])}")
            return self.eExists(indexTuple, edgeCollection, False)
        except:
            raise

    '''
    Adds an Edge to the Directed Graph, where an edge is represented as a pair of 
    string representations of vertices.

    @param  {Collection}    edge    The collection representing the edge.
    @return {Boolean}       True the edge could be added, both to forward edge list and backward edge list.
    '''
    def addEdge(self, edge):
        try:
            return self.__addE(edge, self.E) and self.__addE(self.__class__.reverseEdge(edge), self.backE)
        except:
            raise

    '''
    Internal function that removes a edge from a given internal data structure representing a collection of edges.

    @param  {Collection}    edge            The collection representing a given edge.
    @param  {Collection}    edgeCollection  The internal data structure representing an edge list.
    
    @return {Boolean}       True if the edge could removed from the internal data structure.
    @error  {TypeError}     Raises if the internal data structure does not have the expected functionality.
    '''
    def __removeE(self, edge, edgeCollection):
        try:
            indexTuple = self.__edgeToInternal(edge)
            if isinstance(edgeCollection[indexTuple[0]], list):
                i = 0
            for e in edgeCollection[indexTuple[0]]:
                cur = indexTuple[1:]
                if e == indexTuple[1:]:
                    if isinstance(edgeCollection[indexTuple[0]], list):
                        edgeCollection[indexTuple[0]].pop(i)
                    elif hasattr(edgeCollection[indexTuple[0]], 'remove'):
                        edgeCollection[indexTuple[0]].remove(indexTuple[1:])
                    else:
                        raise TypeError(f"Unable to remove from collection of type {type(edgeCollection[indexTuple[0]])}")
                    return True
                else:
                    if isinstance(edgeCollection[indexTuple[0]], list):
                        i = i + 1
            return False
        except Exception as e:
            raise e

    '''
    Removes an edge from the Graph. Removes the edge from forward and backwards edge lists.

    @param  {Collection}    edge    The collection representing a given edge.

    @return {Boolean}       True if the edge can be removed, False otherwise.
    '''
    def removeEdge(self, edge):
        try:
            #indexTuple = self.__edgeToInternal(edge)
            return self.__removeE(edge, self.E) and self.__removeE(self.__class__.reverseEdge(edge), self.backE)
        except:
            raise


    '''
    Switches a non-empty vertex slot into an empty vertex slot.

    '''
    def __switchVetrex(self, oldIndex, newIndex):
        if self.V[newIndex] == None and self.V[oldIndex] != None:
            for e in self.E[oldIndex]:
                self.__removeE(self.__class__.reverseEdge((oldIndex,) + e), self.backE)
                self.__addE(self.__class__.reverseEdge((newIndex,) + e), self.backE)
            tmp = self.E[newIndex]
            self.E[newIndex] = self.E[oldIndex]
            self.E[oldIndex] = tmp
            tmp = self.V[newIndex]
            self.V[newIndex] = self.V[oldIndex]
            self.V[oldIndex] = tmp
            return True
        else:
            return False

    '''
    Moves the verticies and edges 

    Helper function to the compress function.
    '''
    def __moveEdges(self):
        curIndex = len(self.V) - 1
        while self.unusedV.peek() != None:
            _, nextIndex = self.unusedV.next()
            for i in range(curIndex, nextIndex, -1):
                if self.V == None:
                    continue
                else:
                    if not self.__switchVetrex(i, nextIndex):
                        raise ReferenceError(f"Unable to switch the Verticies at oldIndex: {i} and nextIndex: {nextIndex}")
                    else:
                        curIndex = i - 1
                        i  = nextIndex # break out of inner loop

    '''
    Saves the Graph to a given format.

    Default is JSON for simple abstraction from a given programming language.
    '''
    def __save(self, save_format='json'):
        return json.dumps(self)

    '''
    Compresses the Graph Data Structure to take up less space
    '''
    def compress(self):
        try:
            self.__moveEdges()
        except:
            raise
            

    def merge(self, other):
        raise NotImplementedError("Merge functionality is currently not implemented")


    def serailize(self):
        try:
            self.compress()
            self.__save()
        except:
            raise

    @classmethod
    def __build(cls, vSet=[], eSet=[]):
        """
            Build command to use when building Graphs from serialized data.
            Called by load command after the vertex set and edge set have been extracted from 
            the serialized format.

        """
        graph = cls()
        if isinstance(vSet, list):
            vSet = set(vSet)
        if isinstance(eSet, list):
            eSet = set(eSet)
        for v in vSet:
            graph.addVertex(v)
        for e in eSet:
            graph.addEdge(e)
        return graph

    
    @classmethod
    def load(cls, obj_str, load_format='json'):
        """
            Loads an instance of Graph object from a given string represention
            (either direct string representation or string representation of file)
        """
        if not isinstance(load_format, str) or len(load_format) <= 0:
            raise TypeError(f"Expected load_format to be string, but got {type(load_format)}")
        if load_format in cls.supported_serialize_formats.key():
            if callable(cls.supported_serialize_formats.get(load_format, None)):
                vertex_set, edge_set = cls.supported_serialize_formats[load_format](obj_str)
                return cls.build(vSet=vertex_set, eSet=edge_set)
            else:
                raise TypeError(f"could not call load function for {load_format}, expected function but got: {type(cls.supported_serialize_formats.get(load_format, None))}")
        else:
            raise NotImplementedError(f"Loading format: {load_format} not supported at this time.")