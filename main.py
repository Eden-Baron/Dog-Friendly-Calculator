from calculations.neighborhoods import create_neighborhoods
from calculations.dogs import generate_dogs
from calculations.parks import create_parks
from calculations.calcNearestPark import calcNearestPark
from calculations.rankingCalc import ranking_neighborhoods



neighborhoods_df = create_neighborhoods()
generate_dogs(neighborhoods_df)
create_parks()
calcNearestPark()
ranking_neighborhoods()


