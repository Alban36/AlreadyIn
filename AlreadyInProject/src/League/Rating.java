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
public class Rating {
    
    public Rating()
    {
        this.aRate = 0.0;
    }
    
    /** Adjust the current rate by adding the specified value and return the new rate
     * @param pValue The value to be added to the rate
     * @return The new value of the current rate
     */
    public double AdjustRate(double pValue)
    {
        this.aRate += pValue;
        
        if(this.aRate > this.aMaxRate)
        {
            this.aRate = this.aMaxRate;
        }
        else if(this.aRate < this.aMinRate)
        {
            this.aRate = this.aMinRate;
        }
        
        return this.aRate;
    }
    
    /**
     * Get the value of the current rate
     * @return the current rate
     */
    public double GetRate()
    {
        return this.aRate;
    }
    
    /**
     * Get the maximum value of rating
     * @return the maximum rating possible
     */
    public double GetMaxRate()
    {
        return this.aMaxRate;
    }
    
    /**
     * Get the minimum value of rating
     * @return the minimum value of rating possible
     */
    public double GetMinRate()
    {
        return this.aMinRate;
    }
    
    private double aRate;
    private final double aMaxRate = 100.0;
    private final double aMinRate = 0.0;
}
