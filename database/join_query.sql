SELECT td."gameId", td."playId", td."nflId", 
       gm.week, gm."homeTeamAbbr", gm."visitorTeamAbbr",
	   plr.height, plr.weight, plr."birthDate",
	   plr."collegeName", plr."officialPosition",
	   plr."officialPosition", plr."displayName",
	   pl.quarter, pl.down, pl."yardsToGo", pl."possessionTeam",
	   pl."defensiveTeam", pl."yardlineNumber", pl."gameClock",
	   pl."preSnapHomeScore", pl."preSnapVisitorScore",
	   pl."playResult", pl."offenseFormation",
	   pl."personnelO", pl."defendersInBox", pl."personnelD",
	   pl."dropbackType",  pl."pff_playAction",
	   pl."pff_passCoverage", pl."pff_passCoverageType",
	   pff.pff_role, pff."pff_positionLinedUp", pff.pff_hit,
	   pff.pff_hurry, pff.pff_sack, pff."pff_beatenByDefender",
	   pff."pff_hitAllowed", pff."pff_hurryAllowed",
	   pff."pff_sackAllowed", pff."pff_nflIdBlockedPlayer",
	   pff."pff_blockType", pff."pff_backFieldBlock"
FROM trackingdata as td
LEFT JOIN pffscoutingdata as pff
ON td."gameId" = pff."gameId"
AND td."playId" = pff."playId"
AND td."nflId" = pff."nflId"
LEFT JOIN plays as pl
ON td."gameId" = pl."gameId"
AND td."playId" = pl."playId"
LEFT JOIN games as gm
ON td."gameId" = gm."gameId"
LEFT JOIN players as plr
ON td."nflId" = plr."nflID"
LIMIT 50