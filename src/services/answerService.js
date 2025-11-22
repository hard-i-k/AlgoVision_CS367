import api from './api';

export const answerService = {
  async getAnswersByQuestionId(questionId) {
    const res = await api.get(`/answers/question/${questionId}`);
    return res.data.data.answers;
  },

  async createAnswer(questionId, content) {
    const res = await api.post(`/answers/question/${questionId}`, { content });
    return res.data.data.answer;
  },

  async updateAnswer(id, content) {
    const res = await api.put(`/answers/${id}`, { content });
    return res.data.data.answer;
  },

  async deleteAnswer(id) {
    const res = await api.delete(`/answers/${id}`);
    return res.data;
  },

  async voteAnswer(id, voteType) {
    const res = await api.post(`/answers/${id}/vote`, { voteType });
    return res.data;
  },

  async acceptAnswer(questionId, answerId) {
    const res = await api.put(`/questions/${questionId}/accept/${answerId}`);
    return res.data;
  }
};