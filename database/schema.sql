-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/lEsA9g
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "players" (
    "nflID" int   NOT NULL,
    "height" varchar(10)   NOT NULL,
    "weight" int   NOT NULL,
    "birthDate" date,
    "collegeName" varchar(50),
    "officialPosition" varchar(3)   NOT NULL,
    "displayName" varchar(50)   NOT NULL,
    CONSTRAINT "pk_players" PRIMARY KEY (
        "nflID"
     )
);

CREATE TABLE "games" (
    "gameId" int   NOT NULL,
    "season" int   NOT NULL,
    "week" int   NOT NULL,
    "gameDate" date   NOT NULL,
    "gameTimeEastern" time   NOT NULL,
    "homeTeamAbbr" varchar(3)   NOT NULL,
    "visitorTeamAbbr" varchar(3)   NOT NULL,
    CONSTRAINT "pk_games" PRIMARY KEY (
        "gameId"
     )
);

CREATE TABLE "plays" (
    "gameId" int   NOT NULL,
    "playId" int   NOT NULL,
    "playDescription" varchar(500)   NOT NULL,
    "quarter" int   NOT NULL,
    "down" int   NOT NULL,
    "yardsToGo" int   NOT NULL,
    "possessionTeam" varchar(3)   NOT NULL,
    "defensiveTeam" varchar(3)   NOT NULL,
    "yardlineSide" varchar(3)   NOT NULL,
    "yardlineNumber" int   NOT NULL,
    "gameClock" varchar(5)   NOT NULL,
    "preSnapHomeScore" int   NOT NULL,
    "preSnapVisitorScore" int   NOT NULL,
    "passResult" varchar(2)   NOT NULL,
    "penaltyYards" int   NOT NULL,
    "prePenaltyPlayResult" int   NOT NULL,
    "playResult" int   NOT NULL,
    "foulName1" varchar(100)   NOT NULL,
    "foulNFLId1" int   NOT NULL,
    "foulName2" varchar(100)   NOT NULL,
    "foulNFLId2" int   NOT NULL,
    "foulName3" varchar(100)   NOT NULL,
    "foulNFLId3" int   NOT NULL,
    "absoluteYardlineNumber" int   NOT NULL,
    "offenseFormation" varchar(50)   NOT NULL,
    "personnelO" varchar(50)   NOT NULL,
    "defendersInTheBox" int   NOT NULL,
    "personnelD" varchar(50)   NOT NULL,
    "dropbackType" varchar(50)   NOT NULL,
    "pff_playAction" bool   NOT NULL,
    "pff_passCoverage" varchar(50)   NOT NULL,
    "pff_passCoverageType" varchar(50)   NOT NULL,
    CONSTRAINT "pk_plays" PRIMARY KEY (
        "gameId","playId"
     )
);

CREATE TABLE "pffScoutingData" (
    "gameId" int   NOT NULL,
    "playId" int   NOT NULL,
    "nflId" int   NOT NULL,
    "pff_role" varchar(50)   NOT NULL,
    "pff_positionLinedUp" varchar(10)   NOT NULL,
    "pff_hit" varchar(2)   NOT NULL,
    "pff_hurry" varchar(2)   NOT NULL,
    "pff_sack" varchar(2)   NOT NULL,
    "pff_beatenByDefender" varchar(2)   NOT NULL,
    "pff_hitAllowed" varchar(2)   NOT NULL,
    "pff_hurryAllowed" varchar(2)   NOT NULL,
    "pff_sackAllowed" varchar(2)   NOT NULL,
    "pff_nflIdBlockedPlayer" int   NOT NULL,
    "pff_blockType" varchar(2)   NOT NULL,
    "pff_backFieldBlock" varchar(2)   NOT NULL,
    CONSTRAINT "pk_pffScoutingData" PRIMARY KEY (
        "gameId","playId","nflId"
     )
);

CREATE TABLE "trackingData" (
    "gameId" int   NOT NULL,
    "playId" int   NOT NULL,
    "nflId" int   NOT NULL,
    "frameId" int   NOT NULL,
    "time" timestamp   NOT NULL,
    "jerseyNumber" int   NOT NULL,
    "club" varchar(10)   NOT NULL,
    "playDirection" varchar(5)   NOT NULL,
    "x" float   NOT NULL,
    "y" float   NOT NULL,
    "s" float   NOT NULL,
    "a" float   NOT NULL,
    "dis" float   NOT NULL,
    "o" float   NOT NULL,
    "dir" float   NOT NULL,
    "event" varchar(50)   NOT NULL,
    CONSTRAINT "pk_trackingData" PRIMARY KEY (
        "gameId","playId","nflId"
     )
);

ALTER TABLE "plays" ADD CONSTRAINT "fk_plays_gameId" FOREIGN KEY("gameId")
REFERENCES "games" ("gameId");

ALTER TABLE "pffScoutingData" ADD CONSTRAINT "fk_pffScoutingData_gameId" FOREIGN KEY("gameId")
REFERENCES "games" ("gameId");

ALTER TABLE "pffScoutingData" ADD CONSTRAINT "fk_pffScoutingData_nflId" FOREIGN KEY("nflId")
REFERENCES "players" ("nflID");

ALTER TABLE "pffScoutingData" ADD CONSTRAINT "fk_pffScoutingData_pff_nflIdBlockedPlayer" FOREIGN KEY("pff_nflIdBlockedPlayer")
REFERENCES "players" ("nflID");

ALTER TABLE "trackingData" ADD CONSTRAINT "fk_trackingData_gameId" FOREIGN KEY("gameId")
REFERENCES "games" ("gameId");

