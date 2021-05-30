const dotenv = require('dotenv'); //load .env variables
dotenv.config();

const express = require("express");
const { Pool } = require("pg");
const cors = require("cors");
const axios = require("axios")

const PORT = process.env.PORT

const app = express();
app.disable('x-powered-by');
app.use( express.json());   //only needed if we have POST requests
app.use(cors());            //needed to allow cors

const pool = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD  
})

console.log(process.env.DB_HOST)
console.log(process.env.DB_PORT)
console.log(process.env.DB_NAME)
console.log(process.env.DB_USER)
console.log(process.env.DB_PASSWORD)  
const operators = {
    "eq":"=",
    "ge":">=",
    "le":"<=",
    "in": "IN"
}

// holds column names for each table, only query parameters that are in each specific list will be considered.
const acceptedParams = {
    "listing_location": [
        "id",
        "latitude",
        "longitude",
        "price",
        "borough",
        "village",
        "total_listings_count",
        "is_superhost",
        "guests_included",
        "review_score"
    ],

    "listing_detail": [
        "id",
        "thumbnail_url",
        "medium_url",
        "picture_url",
        "xl_picture_url",
        "name",
        "listing_url",
        "price",
        "summary",
        "space",
        "description",
        "neighborhood_overview",
        "transit",
        "access",
        "host_id",
        "guests_included",
        "number_of_reviews"
    ],   
     
    "listing_other" : [
        "id",
        "square_feet",
        "property_type",
        "room_type",
        "neighbourhood_cleansed",
        "neighbourhood_group_cleansed",
        "minimum_nights",
        "maximum_nights"
    ],

    "listing_reviews" : [
        "id",
        "review_scores_rating",
        "review_scores_accuracy",
        "review_scores_cleanliness",
        "review_scores_checkin",
        "review_scores_communication",
        "review_scores_location",
        "review_scores_value"
    ],
    
    "host" : [
        "host_id",
        "host_location",
        "host_is_superhost",
        "host_neighbourhood",
        "host_listings_count",
        "host_total_listings_count",
        "host_identity_verified",
        "calculated_host_listings_count",
        "calculated_host_listings_count_entire_homes",
        "calculated_host_listings_count_private_rooms",
        "calculated_host_listings_count_shared_rooms"
    ],
    
    "review" : [
        "listing_id",
        "id",
        "date",
        "reviewer_id",
        "reviewer_name",
        "comments"
    ],
    
    "village_category": [
        //"village",
        "age",
        "interest"
    ]
}
function buildQuery(queryString,query,dbParams,setAND=false) {
    /*  Adds WHERE clauses to input queryString, cleans query params
        Inputs: - queryString: A string with a query
                - query: reqest query dict
                - setAND: boolean that should be set to true if there is already a WHERE clause in query
    */
    
    Object.entries(query).forEach(([key, value]) => {
        key = key.split(".");
        if(key.length!=2) {
            return;
        }
        
        if(!(key[1] in operators)) {
            return;
        }
        const colName = key[0].replace(/[";]/g,"")
        if((dbParams.includes(colName))) {
            if(setAND) queryString += " AND ";
            else {
                queryString += " WHERE ";
                setAND=true;
            }
            const operator = operators[key[1]];
            var val;
            if (key[1]!="in") {
                val = value.replace(/[";]/g,"")
                //queryString += `${colName} ${operator} ${val}`
            } else {
                str = '(';
                for(var i=0;i<value.length-1;i++) {
                    str+="'"+value[i].replace(/\+/g," ")+"',";
                }
                str+="'"+value[value.length-1].replace(/\+/g," ")+"')"
                console.log(str)
                val=str
            }
            queryString += `${colName} ${operator} ${val}`
        }
     });
     console.log(queryString)
     return queryString
}

function returnDBResults(error, result,res) {
    if(error) {
        console.log(error);
        res.status(500).send();
    } else {

        res.status(200).send(result.rows);
    }
}

/*
returns locations of all listings
*/
app.get(
    "/listing_location",
    (req,res) => {
        var query = "SELECT * FROM listing_location"
        query = buildQuery(query,req.query,acceptedParams['listing_location']);
        console.log(query)
        pool.query(
            query,
            (error,result) => returnDBResults(error,result,res)
        );        
    }
)
app.get(
    "/listing_location/:id",
    (req,res) => {
        var query = "SELECT * FROM listing_location WHERE id=$1"
        pool.query(
            query,
            [req.params.id],
            (error,result) => returnDBResults(error,result,res)
        )
    }
)

app.get(
    "/listing_detail",
    (req,res) => {
        var query = "SELECT * FROM listing_detail"
        query = buildQuery(query,req.query,acceptedParams['listing_detail'])
        pool.query(
            query,
            (error,result) => returnDBResults(error,result,res)
        )
    }
)
app.get(
    "/listing_detail/:id",
    (req,res) => {
        var query = "SELECT * FROM listing_detail WHERE id=$1"
        pool.query(
            query,
            [req.params.id],
            (error,result) => returnDBResults(error,result,res)
        )
    }
)

app.get(
    "/listing_other",
    (req,res) => {
        var query = "SELECT * FROM listing_other"
        query = buildQuery(query,req.query,acceptedParams['listing_other'])
        pool.query(
            query,
            (error,result) => returnDBResults(error,result,res)
        )
    }
)

app.get(
    "/listing_other/:id",
    (req,res) => {
        var query = "SELECT * FROM listing_other WHERE id=$1"
        pool.query(
            query,
            [req.params.id],
            (error,result) => returnDBResults(error,result,res)
        )
    }
)
app.get(
    "/listing_reviews",
    (req,res) => {
        var query = "SELECT * FROM listing_reviews"
        query = buildQuery(query,req.query,acceptedParams['listing_reviews'])
        pool.query(
            query,
            (error,result) => returnDBResults(error,result,res)
        )
    }
)
app.get(
    "/listing_reviews/:id",
    (req,res) => {
        var query = "SELECT * FROM listing_reviews WHERE id=$1"
        pool.query(
            query,
            [req.params.id],
            (error,result) => returnDBResults(error,result,res)
        )
    }
)
app.get(
    "/host",
    (req,res) => {
        var query = "SELECT * FROM host"
        query = buildQuery(query,req.query,acceptedParams['host'])
        pool.query(
            query,
            (error,result) => returnDBResults(error,result,res)
        )
    }
)
app.get(
    "/host/:id",
    (req,res) => {
        var query = "SELECT * FROM host WHERE host_id=$1"
        pool.query(
            query,
            [req.params.id],
            (error,result) => returnDBResults(error,result,res)
        )
    }
)

/*
returns reviews for listing id
*/
app.get(
    "/reviews",
    (req,res) => {
        console.log(req.query)
        if("id.eq" in req.query)
        {
            console.log("gotcha")
            req.query["listing_id.eq"] = req.query["id.eq"]
            delete req.query["id.eq"]   
        }
        var query = buildQuery(`SELECT * FROM review`,req.query,acceptedParams['review'])
        pool.query(
            query,
            (error,result) => returnDBResults(error,result,res)
        )
    }
)

app.get(
    "/reviews/:id",
    (req,res) => {
        var query = `SELECT * FROM review WHERE id=$1`
        
        pool.query(
            query,
            [req.params.id],
            (error,result) => returnDBResults(error,result,res)
        )
    }
)


app.get(
    "/village_category",
    (req,res) => {
        var query = buildQuery(`SELECT DISTINCT(village) FROM village_category`,req.query,acceptedParams['village_category']);
        pool.query(
            {text:query, rowMode:'array'},
            (error,result) => returnDBResults(error,result,res)
        )
    }
)






if(require.main === module) {
    app.listen(
        PORT,
        () => {
            console.log(`serving from port ${PORT}`);
        }
    )
} else {
    exports.app = app;
}
