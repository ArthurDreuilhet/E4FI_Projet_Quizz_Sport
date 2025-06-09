export default {
  clear() {
		// todo : implement
  },
  savePlayerName(playerName) {
		window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {		
		return window.localStorage.getItem("playerName") || "Player";
  },
  saveParticipationScore(participationScore) {
		// todo : implement
  },
  getParticipationScore() {
		// todo : implement
  }
};