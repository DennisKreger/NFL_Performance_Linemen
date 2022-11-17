-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/lEsA9g
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.



CREATE TABLE "players" (
    "nflID" int   NOT NULL,
    "height" varchar(10),
    "weight" int,
    "birthDate" varchar(10),
    "collegeName" varchar(50),
    "officialPosition" varchar(3),
    "displayName" varchar(50),
    CONSTRAINT "pk_players" PRIMARY KEY (
        "nflID"
     )
);


CREATE TABLE "games" (
    "gameId" int   NOT NULL,
    "season" int,
    "week" int,
    "gameDate" varchar(10),
    "gameTimeEastern" varchar(10),
    "homeTeamAbbr" varchar(3),
    "visitorTeamAbbr" varchar(3),
    CONSTRAINT "pk_games" PRIMARY KEY (
        "gameId"
     )
);

CREATE TABLE "plays" (
    "gameId" int   NOT NULL,
    "playId" int   NOT NULL,
    "playDescription" varchar(1000),
    "quarter" int,
    "down" int,
    "yardsToGo" int,
    "possessionTeam" varchar(3),
    "defensiveTeam" varchar(3),
    "yardlineSide" varchar(3),
    "yardlineNumber" int,
    "gameClock" varchar(5),
    "preSnapHomeScore" int,
    "preSnapVisitorScore" int,
    "passResult" varchar(2),
    "penaltyYards" int,
    "prePenaltyPlayResult" int,
    "playResult" int,
    "foulName1" varchar(100),
    "foulNFLId1" int,
    "foulName2" varchar(100),
    "foulNFLId2" int,
    "foulName3" varchar(100),
    "foulNFLId3" int,
    "absoluteYardlineNumber" int,
    "offenseFormation" varchar(50),
    "personnelO" varchar(50),
    "defendersInBox" int,
    "personnelD" varchar(50),
    "dropbackType" varchar(50),
    "pff_playAction" int,
    "pff_passCoverage" varchar(50),
    "pff_passCoverageType" varchar(50),
    CONSTRAINT "pk_plays" PRIMARY KEY (
        "gameId","playId"
     )
);

CREATE TABLE "pffscoutingdata" (
    "gameId" int   NOT NULL,
    "playId" int   NOT NULL,
    "nflId" int  NOT NULL,
    "pff_role" varchar(50)   NOT NULL,
    "pff_positionLinedUp" varchar(10)   NOT NULL,
    "pff_hit" int,
    "pff_hurry" int,
    "pff_sack" int,
    "pff_beatenByDefender" int,
    "pff_hitAllowed" int,
    "pff_hurryAllowed" int,
    "pff_sackAllowed" int,
    "pff_nflIdBlockedPlayer" int,
    "pff_blockType" varchar(2),
    "pff_backFieldBlock" int,
    CONSTRAINT "pk_pffscoutingdata" PRIMARY KEY (
        "gameId","playId","nflId"
     )
);

CREATE TABLE "trackingdata" (
    "gameId" int   NOT NULL,
    "playId" int   NOT NULL,
    "nflId" int,
    "frameId" int   NOT NULL,
    "time" timestamp,
    "jerseyNumber" int,
    "team" varchar(10),
    "playDirection" varchar(5),
    "x" float,
    "y" float,
    "s" float,
    "a" float,
    "dis" float,
    "o" float,
    "dir" float,
    "event" varchar(50)
);

CREATE TABLE "combine" (
    "player" varchar(50)   NOT NULL,
    "pos" varchar(5),
    "school" varchar(50),
    "ht" varchar(10),
    "wt" int,
    "40yd" float,
    "vertical" float,
    "bench" int,
    "broadjump" int,
    "3cone" float,
    "shuttle" float,
    "team" varchar(50),
    "round" int,
    "pick" int,
    "year" int
);

DROP TABLE players
DROP TABLE games
DROP TABLE plays
DROP TABLE pffscoutingdata
DROP TABLE trackingdata
DROP TABLE combine

SELECT * FROM players
SELECT * FROM games
SELECT * FROM plays
SELECT * FROM pffscoutingdata
SELECT * FROM trackingdata LIMIT 50
SELECT * FROM combine

SELECT COUNT(*) FROM players
SELECT COUNT(*) FROM games
SELECT COUNT(*) FROM plays
SELECT COUNT(*) FROM pffscoutingdata
SELECT COUNT(*) FROM trackingdata
SELECT COUNT(*) FROM combine

ALTER TABLE "plays" ADD CONSTRAINT "fk_plays_gameId" FOREIGN KEY("gameId")
REFERENCES "games" ("gameId");

ALTER TABLE "pffscoutingdata" ADD CONSTRAINT "fk_pffscoutingdata_gameId" FOREIGN KEY("gameId")
REFERENCES "games" ("gameId");

ALTER TABLE "pffscoutingdata" ADD CONSTRAINT "fk_pffscoutingdata_nflId" FOREIGN KEY("nflId")
REFERENCES "players" ("nflID");

ALTER TABLE "pffdscoutingData" ADD CONSTRAINT "fk_pffscoutingData_pff_nflIdBlockedPlayer" FOREIGN KEY("pff_nflIdBlockedPlayer")
REFERENCES "players" ("nflID");

ALTER TABLE "trackingdata" ADD CONSTRAINT "fk_trackingdata_gameId" FOREIGN KEY("gameId")
REFERENCES "games" ("gameId");



GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dennis;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO liam;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO greg;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO robert;