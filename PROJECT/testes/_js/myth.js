
function
/*class*/ Myth(id, sname, fname, alias, tier, join, race, skill, badges){

// Attributes
    var __id, __shortName, __fullName, __alias, __tier, __join, __race, __skill, __badges;
    __id = id || "no_id";
    __shortName = sname || "no_name";
    __fullName = fname || "no_full_name";
    __alias = alias || "no_alias";
    __tier = tier || new Tier();
    __join = join || new Date();
    __race = race || "no_race";
    __skill = skill || "no_skill";
    __badges = badges || [];

// Methods
    this.setId = function(id){
        __id = id;
    }
    this.getId = function(){
        return __id;
    }

    this.setShortName = function(name){
        __shortName = name;
    }
    this.getShortName = function(){
        return __shortName;
    }

    this.setFullName = function(fname){
        __fullName = fname;
    }
    this.getFullName = function(){
        return __fullName;
    }

    this.setAlias = function(alias){
        __alias = alias;
    }
    this.getAlias = function(){
        return __alias;
    }

    this.getTagId = function(){
        return "id-"+__id;
    }

    this.setTier = function(tier){
        __tier = tier;
    }
    this.getTier = function(){
        return __tier;
    }

    this.setJoinDate = function(joindate){
        __join = joindate;
    }
    this.getJoinDate = function(){
        return __join;
    }

    this.setRace = function(race){
        __race = race;
    }
    this.getRace = function(){
        return __race;
    }

    this.setSkill = function(skill){
        __skill = skill;
    }
    this.getSkill = function(){
        return __skill;
    }

    this.setBadges = function(badges){
        __badges = badges;
    }
    this.getBadges = function(){
        return __badges;
    }
    this.addBadge = function(badge){
        __badges.push(badge);
    }
}
