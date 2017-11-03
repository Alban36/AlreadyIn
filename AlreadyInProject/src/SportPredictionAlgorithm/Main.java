/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package SportPredictionAlgorithm;

import League.Team;

/**
 *
 * @author alban
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Team LAL = new Team("Lakers","Los Angeles");
        System.out.print(LAL.GetTeamName()+"\n");
    }
    
}
