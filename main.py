from neighborhoods import create_neighborhoods
from dogs import generate_dogs
from parks import create_parks
from calcNearestPark import calcNearestPark
from rankingCalc import ranking_neighborhoods 
import pandas as pd

def main():
    neighborhoods_df = create_neighborhoods()

    generate_dogs(neighborhoods_df)

    create_parks()

    calcNearestPark()

    ranking_neighborhoods()
    rank_df = pd.read_csv("data/rank_for_neighborhoods.csv")

    print("ברוך הבא למערכת דירוג השכונות לכלבים בתל אביב")
    name = input(f"הכנס שם שכונה מאחד השמות הבאים: {', '.join(rank_df['neighborhoodName'].tolist())} \n ליציאה הקלד יציאה \n")

    while True:
        if name == "יציאה":
            break

        match = rank_df[rank_df["neighborhoodName"].str.contains(name, case=False, na=False)]
        if not match.empty:
            rating = match.iloc[0]["rating"]
            print(f"דירוג השכונה '{match.iloc[0]['neighborhoodName']}': {rating}")
            break
        else:
            print("לא נמצאה שכונה בשם הזה. נסה שוב.")
            name = input(f"הכנס שם שכונה מאחד השמות הבאים: {', '.join(rank_df['neighborhoodName'].tolist())} \n ליציאה הקלד יציאה \n")

if __name__ == "__main__":
    main()
