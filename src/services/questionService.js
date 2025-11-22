import api from './api';

export const questionService = {
  async getAllQuestions() {
    const res = await api.get('/questions');
    return res.data.data.questions;
  },

  async getQuestionById(id) {
    const res = await api.get(`/questions/${id}`);
    return res.data.data.question;
  },

  async createQuestion(questionData) {
    try {
      const res = await api.post('/questions', questionData);
      return res.data.data.question;
    } catch (error) {
      console.error('Question creation error:', error.response?.data || error.message);
      throw error;
    }
  },

  async updateQuestion(id, questionData) {
    const res = await api.put(`/questions/${id}`, questionData);
    return res.data.data.question;
  },

  async deleteQuestion(id) {
    const res = await api.delete(`/questions/${id}`);
    return res.data;
  },

  async voteQuestion(id, voteType) {
    // Assuming backend has /questions/:id/vote endpoint
    const res = await api.post(`/questions/${id}/vote`, { voteType });
    return res.data;
  }
};