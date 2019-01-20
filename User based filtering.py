

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # users item ratings data is expected in the form of a nested dictionary:
    # at the top level, it has User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
 
    def __init__(self, usersItemRatings, k=1):
        
      
        self.usersItemRatings = usersItemRatings
            
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
       
    #################################################
    # calcualte the pearson correlation between two item ratings dictionaries userXItemRatings and userYItemRatings
    # userXItemRatings and userYItemRatings data is expected in the form of dictionaries of item ratings
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        self.userXItemRatings = userXItemRatings
        self.userYItemRatings = userYItemRatings
        
        distance = 0
        sumxy = 0
        sumx = 0
        sumy = 0
        sumx2 = 0
        sumy2 = 0
        Xset = set(userXItemRatings)
        Yset = set(userYItemRatings) 
        n = len(Xset.intersection(Yset))
        if n == 0:
            return -2
        
        for i in userXItemRatings.keys():
            if i in userYItemRatings.keys():
                x = userXItemRatings[i]
                y = userYItemRatings[i]
                sumxy += x*y
                sumx += x
                sumx2 += pow(x,2)
                sumy += y
                sumy2 += pow(y,2)
     
        denom = (pow(sumx2-(pow(sumx,2)/n),1/2))*(pow(sumy2-(pow(sumy,2)/n),1/2))
        if denom == 0:
            return -2
        
        distance = round(((sumxy - (sumx*sumy)/n)/denom),2)
        return distance 
        
    def KNN(self, userX):
        
        self.userX = self.usersItemRatings[userX]
        
        dist = []
        
            
        for user in self.usersItemRatings:
             if self.usersItemRatings[user] != userX:
                distance = self.pearsonFn(self.usersItemRatings[userX],self.usersItemRatings[user])
                if distance != 1: # remove values equal to 1 so the user does not use itself for recommendation
                    
                    dist.append((user, distance)) 
               
        dist.sort(key=lambda x:x[1], reverse=True)
    
        return dist
   
    
    #################################################
    # make recommendations for userX from the k most similar nearest neigibors (NNs)
    def recommendKNN(self, userX):

        self.userX = self.usersItemRatings[userX]
        Uratings = self.usersItemRatings[userX]
        
        knn = self.KNN(userX)
        knnsum = 0.0
        
        for k in range(self.k):
            knnsum +=((knn[k][1])+1)/2 #Correct for negative's
        
        recs = {}
        for user in range(self.k):
            weight = (((knn[user][1])+1)/2) / knnsum
            
            Nratings = self.usersItemRatings[knn[user][0]]
            
            for i in Nratings:
                if i not in Uratings:
                    if i not in recs:
                        recs[i] = (Nratings[i]*weight)
                    else:
                        recs[i] = (recs[i]+Nratings[i]*weight)
          
        recs = list(recs.items())
        recs.sort(key=lambda x:x[1],reverse=True)
        return recs
          



        
       



        