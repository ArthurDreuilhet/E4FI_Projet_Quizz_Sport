import axios from 'axios'

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
  getQuestion(position) {
    // not implemented
  },
}
