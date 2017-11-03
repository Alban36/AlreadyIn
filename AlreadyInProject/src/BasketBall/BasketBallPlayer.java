/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package BasketBall;

import League.Player;

/**
 *
 * @author alban
 */
public class BasketBallPlayer extends Player {
    public BasketBallPlayer(String pName)
    {
        super(pName);
        
        this.aGamesPlayed=0;
        this.aPoints=0;
        this.aMinutesPlayed=0;
        this.aFieldGoalTaken=0;
        this.aFieldGoalScored=0;
        this.a3PtsTaken=0;
        this.a3PtsScored=0;
        this.aFreeThrowTaken=0;
        this.aFreeThrowScored=0;
        this.aAssists=0;
        this.aTurnOvers=0;
        this.aDefensiveRebounds=0;
        this.aOffensiveRebounds=0;
        this.aSteals=0;
        this.aBlockedShots=0;
    }
    
    @Override
    public double CalculateGlobalRating()
    {
        return super.CalculateGlobalRating();
    }
    
    int aGamesPlayed;
    int aPoints;
    int aMinutesPlayed;
    int aFieldGoalTaken;
    int aFieldGoalScored;
    int a3PtsTaken;
    int a3PtsScored;
    int aFreeThrowTaken;
    int aFreeThrowScored;
    int aAssists;
    int aTurnOvers;
    int aDefensiveRebounds;
    int aOffensiveRebounds;
    int aSteals;
    int aBlockedShots;
}
