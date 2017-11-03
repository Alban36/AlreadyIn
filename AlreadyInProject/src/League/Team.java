/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package League;

/**
 * Class that defines what a team is
 * @author alban
 */
public class Team {
    public Team(String pName, String pLocation)
    {
        this.aName = pName;
        this.aLocation = pLocation;
        this.aGlobalRate = new Rating();
    }
    
    /**
     * Get the team name
     * @return the team name
     */
    public String GetTeamName()
    {
        return this.aName;
    }
    
    /**
     * Get the team location
     * @return the team location
     */
    public String GetTeamLocation()
    {
        return this.aLocation;
    }
    
    /**
     * Get the team rating
     * @return the current team rating
     */
    public double GetTeamRating()
    {
        return this.aGlobalRate.GetRate();
    }
    
    /**
     * Adjust the current team rating
     * @param pValue
     * @return return the new team rating
     */
    public double AdjustTeamRating(double pValue)
    {
        return this.aGlobalRate.AdjustRate(pValue);
    }
    
    private final String aName;
    private final String aLocation;
    private Rating aGlobalRate;
}
