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
  save_Tokken(token) {
    window.localStorage.setItem("token", token);
  },
  get_Token() {
    return window.localStorage.getItem("token") || null;
  },
  saveParticipationScore(participationScore) {
		// todo : implement
  },
  getParticipationScore() {
		// todo : implement
  }
};