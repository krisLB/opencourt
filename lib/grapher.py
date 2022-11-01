import networkx as nx
from networkx.readwrite import json_graph
import json
import re
#import matplotlib.pyplot as plt
from . import helper

#Class for converting Case Citations into Graph
class GraphBuilder(object):
    """Class to build the network graph using networkX module"""
    def __init__(self, caseDict, outfile, gml, baseURL):
      self.caseDict = caseDict
      self.outfile = outfile
      self.gml = gml
      self.baseURL = baseURL

    def getYear(self, dat):
      """Extract the Year from the Case Date"""
      if dat:
        yrs = re.findall(r'(?<= )\d{1,4}$', dat)
        return int(yrs[0])
      else:
        return 0

    def drawGraph(self):
         """Build a Network graph from the citations in a json-derived dictionary"""
         print('Grapher: Drawing network')
         G=nx.Graph()
         cD = self.caseDict
         print(f'   Number of Cases: {len(cD)}')
         #Iterate through cases to create Nodes and a volume dictionary to check cases against
         for case in cD:
              #nodeN= str(case['number'][0])
              c = case['number']
              nodeN= str(c)
              yr = self.getYear(case['date'])
              G.add_node(nodeN, name=case['name'], url=self.baseURL+case['url'], vol=case['vol'], d=case['date'], year=yr)
              #Iterate through cases to build edges
              for cite in case['citations']:
                  targ = str(cite)
                  G.add_edge(nodeN, targ)

         if self.gml in ['g','a']:
              nx.write_gml(G,'vis/'+self.outfile+'.gml')
              nx.write_gml(G,'vis/'+self.outfile+'.gml.gz')
         if self.gml in ['j','a']:
              d = json_graph.node_link_data(G)
              json.dump(d, open('vis/'+self.outfile+'.json','w'))
         #nx.draw(G)
         #plt.savefig("network.png")
         print('Grapher: Done')
