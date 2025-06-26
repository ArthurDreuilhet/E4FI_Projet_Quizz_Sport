import axios from 'axios'
import Participation_storage_service from './Participation_storage_service'

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
})

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      'Content-Type': 'application/json',
    }
    if (token != null) {
      headers.authorization = 'Bearer ' + token
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data }
      })
      .catch((error) => {
        console.error(error)
      })
  },
  async getInfos() {
    try {
      const response = await fetch('http://localhost:5000/quiz-info')
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      return data
    }
    catch (error) {
      console.error('There has been a problem with your fetch operation:', error)
      return null
    }
  },
  async get_login(password) {
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + Participation_storage_service.get_Token(),
        },
        body: JSON.stringify({ "password": password }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      return data;

    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
      return null;
    }
  },
  async get_Question (id) {
    try {
      const response = await fetch(`http://localhost:5000/questions/${id}`);
      const question = await response.json();

      console.log('Fetched question:', question);

      return question;

    } catch (error) {
      console.error('Error fetching question:', error);
    }
  },
  async post_participations(playerName, playerAnswer) {
    try {
      const response = await fetch('http://localhost:5000/participations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "playerName": playerName,
          "answers": playerAnswer
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Participation posted successfully:', data);
      return { playerName: data.playerName, score: data.score };
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
      return null;
    }
  },
  async get_all_participations() {
    try {
      const response = await fetch('http://localhost:5000/participations', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('All participations fetched successfully:', data);
      return data.participants;
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
      return null;
    }
  },
  
  // Méthodes d'administration
  async post_question(questionData, token) {
    try {
      const response = await fetch('http://localhost:5000/questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(questionData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error creating question:', error);
      return null;
    }
  },

  async update_question(questionId, questionData, token) {
    try {
      const response = await fetch(`http://localhost:5000/questions/${questionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(questionData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('Error updating question:', error);
      return false;
    }
  },

  async delete_question(questionId, token) {
    try {
      const response = await fetch(`http://localhost:5000/questions/${questionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('Error deleting question:', error);
      return false;
    }
  },

  async delete_all_questions(token) {
    try {
      const response = await fetch('http://localhost:5000/questions/all', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('Error deleting all questions:', error);
      return false;
    }
  },

  async delete_all_participants(token) {
    try {
      const response = await fetch('http://localhost:5000/participations/all', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('Error deleting all participants:', error);
      return false;
    }
  },

  async get_question_by_position(position) {
    try {
      const response = await fetch(`http://localhost:5000/questions?position=${position}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching question by position:', error);
      return null;
    }
  },

  async rebuild_database(token) {
    try {
      const response = await fetch('http://localhost:5000/rebuild-db', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return true;
    } catch (error) {
      console.error('Error rebuilding database:', error);
      return false;
    }
  },
}
