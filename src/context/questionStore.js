import { create } from 'zustand';
import { questionService } from '../services/questionService';
import { answerService } from '../services/answerService';

export const useQuestionStore = create((set, get) => ({
  questions: [],
  currentQuestion: null,
  answers: [],
  isLoading: false,
  error: null,

  fetchQuestions: async () => {
    set({ isLoading: true, error: null });
    try {
      const questions = await questionService.getAllQuestions();
      set({ questions: Array.isArray(questions) ? questions : [], isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false, questions: [] });
    }
  },

  fetchQuestionById: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const question = await questionService.getQuestionById(id);
      const answers = await answerService.getAnswersByQuestionId(id);
      
      set({
        currentQuestion: question,
        answers: Array.isArray(answers) ? answers : [],
        isLoading: false
      });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  createQuestion: async (questionData) => {
    set({ isLoading: true, error: null });
    try {
      const newQuestion = await questionService.createQuestion(questionData);
      const currentQuestions = get().questions || [];
      const questions = [newQuestion, ...currentQuestions];
      
      set({
        questions,
        isLoading: false
      });
      
      return newQuestion;
    } catch (error) {
      console.error('Store error creating question:', error);
      const errorMessage = error.response?.data?.message || error.message || 'Failed to create question';
      set({ error: errorMessage, isLoading: false });
      throw new Error(errorMessage);
    }
  },

  createAnswer: async (answerData) => {
    set({ isLoading: true, error: null });
    try {
      const newAnswer = await answerService.createAnswer(answerData);
      const currentAnswers = get().answers || [];
      const answers = [...currentAnswers, newAnswer];
      
      set({
        answers,
        isLoading: false
      });
      
      return newAnswer;
    } catch (error) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  voteQuestion: async (id, voteType) => {
    try {
      await questionService.voteQuestion(id, voteType);
      
      const currentQuestions = get().questions || [];
      const questions = currentQuestions.map(q =>
        q.id === id
          ? { ...q, votes: (q.votes || 0) + (voteType === 'up' ? 1 : -1) }
          : q
      );
      
      const currentQuestion = get().currentQuestion;
      if (currentQuestion && currentQuestion.id === id) {
        set({
          currentQuestion: {
            ...currentQuestion,
            votes: (currentQuestion.votes || 0) + (voteType === 'up' ? 1 : -1)
          }
        });
      }
      
      set({ questions });
    } catch (error) {
      console.error('Failed to vote question:', error);
    }
  },

  voteAnswer: async (id, voteType) => {
    try {
      await answerService.voteAnswer(id, voteType);
      
      const currentAnswers = get().answers || [];
      const answers = currentAnswers.map(a =>
        a.id === id
          ? { ...a, votes: (a.votes || 0) + (voteType === 'up' ? 1 : -1) }
          : a
      );
      
      set({ answers });
    } catch (error) {
      console.error('Failed to vote answer:', error);
    }
  },

  acceptAnswer: async (id) => {
    try {
      await answerService.acceptAnswer(id);
      
      const currentAnswers = get().answers || [];
      const answers = currentAnswers.map(a => ({
        ...a,
        isAccepted: a.id === id
      }));
      
      set({ answers });
    } catch (error) {
      console.error('Failed to accept answer:', error);
    }
  }
}));