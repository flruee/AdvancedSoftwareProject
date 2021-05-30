from sqlalchemy import create_engine
import psycopg2 as pg
import pandas as pd
import io
import numpy as np


USER="postgres"
HOST="localhost"
PORT= '5433'
DB_NAME="ase"
PASSWORD="turmturm"
engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")



def createTables():
    print("Creating tables")
    conn = pg.connect(f"user={USER} dbname={DB_NAME} password={PASSWORD} port={PORT}")
    cur = conn.cursor()
    debug=False

    cur.execute("Drop table village_category")
    if not debug:
        cur.execute(
            """
            create table if not exists listing_location (
                id integer primary key,
                latitude decimal,
                longitude decimal,
                price integer,
                borough varchar(13),
                village varchar(26),
                total_listings_count integer,
                is_superhost boolean,
                guests_included integer,
                review_score decimal
            )
            """
        )
        cur.execute(
            """
            create table if not exists village_category(
                village varchar(26),
                age varchar(10),
                interest varchar(11),
                primary key (village,age,interest)
            )
            """
        )
        cur.execute(
            """
            create table if not exists listing_detail (
                id integer primary key,
                thumbnail_url varchar(100),
                medium_url varchar(100),
                picture_url varchar(100),
                xl_picture_url varchar(100),
                name varchar(200),
                listing_url varchar(100),
                price integer,
                summary text,
                space text,
                description text,
                neighborhood_overview text,
                transit text,
                access text,
                host_id integer,
                guests_included integer,
                number_of_reviews integer
            )
            """
        )
        cur.execute(
            """
            create table if not exists listing_other (
                id integer primary key,
                square_feet integer,
                property_type varchar(50),
                room_type varchar(50),
                neighbourhood_cleansed varchar(50),
                neighbourhood_group_cleansed varchar(50),
                minimum_nights integer,
                maximum_nights integer
            )
            """
        )
        
        cur.execute(
            """
            create table if not exists listing_reviews (
                id integer primary key,
                review_scores_rating decimal,
                review_scores_accuracy decimal,
                review_scores_cleanliness decimal,
                review_scores_checkin decimal,
                review_scores_communication decimal,
                review_scores_location decimal,
                review_scores_value decimal
            )
            """
        )
        cur.execute(
        """
            create table if not exists host(
                host_id integer primary key,
                host_location text,
                host_is_superhost varchar(1),
                host_neighbourhood text,
                host_listings_count integer,
                host_total_listings_count integer,
                host_identity_verified varchar(1),
                calculated_host_listings_count integer,
                calculated_host_listings_count_entire_homes integer,
                calculated_host_listings_count_private_rooms integer,
                calculated_host_listings_count_shared_rooms integer
            )
            """
        )
        cur.execute(
            """
            create table if not exists review (
                listing_id integer,
                id integer primary key,
                date date,
                reviewer_id integer,
                reviewer_name varchar(100),
                comments text
            )
            """
        )
    conn.commit()
    conn.close()

def addListingsAndHost(path):
    engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")
    df = pd.read_csv(path)

    listing_location = df[[
        'id',
        'latitude',
        'longitude',
        'price',
        'neighbourhood_group_cleansed', #borough
        'neighbourhood_cleansed', #village
        'host_total_listings_count',
        'host_is_superhost',
        'guests_included',
        'review_scores_rating'
        ]]
    
    for col in listing_location.columns:
        print(f"{col}: {listing_location[col].isnull().sum()}")
        if(col in ['host_total_listings_count','review_scores_rating']):
            listing_location[col].fillna(0.0,inplace=True)
        elif(col in ['host_is_superhost']):
            listing_location[col].fillna('f',inplace=True)
    
    #change price dtype
    listing_location['price'] = listing_location['price'].str.replace("$",'').str.replace(",",'').str.replace('.00','')
    listing_location.loc[listing_location['price']=='','price'] = 0
    listing_location['price'] = listing_location['price'].astype(np.int32)
    #change superhost dtype
    listing_location['host_is_superhost'] = listing_location['host_is_superhost'].map({"f":False,"t":True})
    listing_location['host_total_listings_count'] = listing_location['host_total_listings_count'].astype(int)
    for col in listing_location.columns:
        print(f"{col}: {type(listing_location.at[0,col])}")
    streamData(listing_location,'listing_location')
    """
    listing_detail = df[[
        'id',
        'thumbnail_url',
        'medium_url',
        'picture_url',
        'xl_picture_url',
        'name',
        'listing_url',
        'price',
        'summary',
        'space',
        'description',
        'neighborhood_overview',
        'transit',
        'access',
        'host_id',
        'guests_included',
        'number_of_reviews']]
    listing_detail = replaceNewline(listing_detail,'name')
    listing_detail = replaceNewline(listing_detail,'summary')
    listing_detail = replaceNewline(listing_detail,'space')
    listing_detail = replaceNewline(listing_detail,'description')
    listing_detail = replaceNewline(listing_detail,'neighborhood_overview')
    listing_detail = replaceNewline(listing_detail,'transit')
    listing_detail = replaceNewline(listing_detail,'access')
    listing_detail['price'] = listing_detail['price'].str.replace("$",'').str.replace(",",'').str.replace('.00','')
    listing_detail.loc[listing_detail['price']=='','price'] = 0
    listing_detail['price'] = listing_detail['price'].astype(np.int32)
    listing_detail = listing_detail.drop([20395,32319,41689,42208],axis=0)
    streamData(listing_detail,'listing_detail')

    listing_other = df[[
        'id',
        'square_feet',
        'property_type',
        'room_type',
        'neighbourhood_cleansed',
        'neighbourhood_group_cleansed',
        'minimum_nights',
        'maximum_nights'
    ]]
    listing_other['square_feet'].fillna(0,inplace=True)
    listing_other['square_feet'] = listing_other['square_feet'].astype(np.int32)

    streamData(listing_other,"listing_other")
    
    listing_reviews = df[[
        'id',
        'review_scores_rating',
        'review_scores_accuracy',
        'review_scores_cleanliness',
        'review_scores_checkin',
        'review_scores_communication',
        'review_scores_location',
        'review_scores_value',
    ]]
    streamData(listing_reviews,"listing_reviews")
    
    host = df[[
        'host_id',
        'host_location',
        'host_is_superhost',
        'host_neighbourhood',
        'host_listings_count',
        'host_total_listings_count',
        'host_identity_verified',
        'calculated_host_listings_count',
        'calculated_host_listings_count_entire_homes',
        'calculated_host_listings_count_private_rooms',
        'calculated_host_listings_count_shared_rooms'
    ]]

    host.drop_duplicates("host_id","first",inplace=True)
    host.fillna("",inplace=True)
    for column in host.columns[1:]:
        try:
            host[column] = host[column].astype(str)
            host[column] = host[column].str.replace(".0","").str.replace(".00","")
        except:
            pass

    
    streamData(host,'host')
    """
    print("done")

def addReviews(path):
    df = pd.read_csv(path)
    print(df.columns)
    df.drop([3225,109556,162758,409475,624461,710672,822878],axis=0,inplace=True)
    df.reset_index(inplace=True,drop=True)
    print(f"deleting unnecessary chars in {path} in column reviewer_name")
    df = deleteUnnecessaryChars(df,"reviewer_name")
    print(f"Replacing newline chars in {path} in column comments")
    df = replaceNewline(df,'comments')
    #bad encoding
    df.at[162758,"comments"] = df.at[162758,'comments'].replace("—\\0",",")
    df.at[822878,"comments"] = df.at[822878,'comments'].replace("—\\0",",")

    #Emojis don't seem compatible with postgres -.-
    df.at[624461,"comments"] = df.at[624461,"comments"].replace(":-)","").replace(":-\\","")
    print("done")
    streamData(df,"review")

def streamData(df,tableName="None"):
    print("Start loading data into db")
    engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()


    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, tableName, null="") # null values become ''
    conn.commit()
    print(f"table {tableName} complete")




def replaceNewline(df,column):
    """
    transforns \n to \\n, \r to \\r and \t with nothing because sql has a problem with it
    """
    for i in range(len(df[column])):
        try:
            df.at[i,column] = df.at[i,column].replace("\n","\\n").replace("\r","\\r").replace("\t","")
        except AttributeError:
            pass
    
    return df

def deleteUnnecessaryChars(df,column):
    """
    transforns \n to \\n, \r to \\r and \t with nothing because sql has a problem with it
    """
    for i in range(len(df[column])):
        try:
            df.at[i,column] = df.at[i,column].replace("\n","").replace("\r","").replace("\t","").replace("(","").replace(")","")
        except AttributeError:
            pass
    
    return df


def addNeighborhood():
    df = pd.read_csv("neighborhood_activity.csv")
    streamData(df,"village_category")
    
if __name__=="__main__":
    
    createTables()
    #addListingsAndHost("data/listings.csv")
    #addReviews("data/reviews.csv")
    addNeighborhood()









