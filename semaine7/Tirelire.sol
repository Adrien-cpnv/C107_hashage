// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TirelireMonoUtilisateur {

    address public proprietaire;
    uint public dateRetrait;

    constructor() {
        proprietaire = msg.sender;
    }

    // Déposer de l'argent avec une date de retrait
    function deposer(uint _dateRetrait) external payable {
        require(msg.sender == proprietaire, "Seul le proprietaire peut deposer");
        require(msg.value > 0, "Montant nul interdit");
        require(_dateRetrait > block.timestamp, "La date doit etre dans le futur");
        dateRetrait = _dateRetrait;
    }

    // Retirer après la date
    function retirer() external {
        require(msg.sender == proprietaire, "Seul le proprietaire peut retirer");
        require(address(this).balance > 0, "Aucun fond a retirer");
        require(block.timestamp >= dateRetrait, "Date de retrait passee non atteinte");

        uint montant = address(this).balance;
        (bool succes, ) = proprietaire.call{value: montant}("");
        require(succes, "Echec de l'envoi");
    }

    // Voir le montant déposé
    function getDepot() external view returns (uint) {
        return address(this).balance;
    }

    // Voir la date de retrait
    function getDateRetrait() external view returns (uint) {
        return dateRetrait;
    }

    // Bloque les dépôts directs non contrôlés
    receive() external payable {
        revert("Utiliser la fonction deposer");
    }
}