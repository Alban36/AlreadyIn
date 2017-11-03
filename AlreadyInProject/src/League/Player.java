/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package League;

/**
 *
 * @author alban
 */
public class Player {
    public Player(String pName)
    {
        this.aName = pName;
        this.aGlobalRate = new Rating();
    }
    
    public double CalculateGlobalRating()
    {
        return this.aGlobalRate.GetRate();
    }
    
    private final String aName;
    private Rating aGlobalRate;
}
