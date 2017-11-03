/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package League;

import java.util.Vector;

/**
 *
 * @author alban
 */
public class Roster {
    public Roster()
    {
        this.aMainRoster = new Vector();
        this.aInjuredList = new Vector();
        this.aTwoWayContracts = new Vector(this.aNbTwoWayContract);
    }
    
    /**
     * Add a player to the roster
     * @param pPlayer the player to add to the roster
     */
    public void AddPlayerToMainRoster(Player pPlayer)
    {
        aInjuredList.remove(pPlayer); //make sure the player is removed from the injured list
        aMainRoster.add(pPlayer);
    }
    
    private Vector aMainRoster;
    private Vector aInjuredList;
    private Vector aTwoWayContracts;
    private final int aMaxPlayer = 15;
    private final int aNbTwoWayContract = 2;
}
