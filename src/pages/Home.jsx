import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useQuestionStore } from '../context/questionStore';
import { useAuthStore } from '../context/authStore';
import QuestionCard from '../components/Questions/QuestionCard';
import Button from '../components/UI/Button';
import Spinner from '../components/UI/Spinner';
import { PlusIcon } from '@heroicons/react/24/outline';

const Home = () => {
  const { questions = [], isLoading, fetchQuestions } = useQuestionStore();
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    fetchQuestions();
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">All Questions</h1>
          <p className="text-gray-600 mt-1">
            {questions?.length || 0} questions
          </p>
        </div>
        
        {isAuthenticated && (
          <Link to="/ask" className="mt-4 sm:mt-0">
            <Button className="flex items-center space-x-2">
              <PlusIcon className="h-5 w-5" />
              <span>Ask Question</span>
            </Button>
          </Link>
        )}
      </div>

      {/* Questions list */}
      {!questions || questions.length === 0 ? (
        <div className="text-center py-12">
          <div className="max-w-md mx-auto">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No questions yet
            </h3>
            <p className="text-gray-600 mb-6">
              Be the first to ask a question and get the discussion started!
            </p>
            {isAuthenticated ? (
              <Link to="/ask">
                <Button>Ask the first question</Button>
              </Link>
            ) : (
              <div className="space-y-2">
                <p className="text-sm text-gray-500">
                  Sign in to ask questions
                </p>
                <div className="flex justify-center space-x-3">
                  <Link to="/login">
                    <Button variant="outline" size="sm">Sign in</Button>
                  </Link>
                  <Link to="/register">
                    <Button size="sm">Sign up</Button>
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {Array.isArray(questions) && questions.map((question) => (
            <QuestionCard key={question.id} question={question} />
          ))}
        </div>
      )}

      {/* Call to action for guests */}
      {!isAuthenticated && questions && questions.length > 0 && (
        <div className="mt-12 bg-blue-50 rounded-lg p-8 text-center">
          <h3 className="text-lg font-medium text-blue-900 mb-2">
            Join the StackIt Community
          </h3>
          <p className="text-blue-800 mb-6">
            Sign up to ask questions, post answers, and participate in discussions.
          </p>
          <div className="flex justify-center space-x-3">
            <Link to="/register">
              <Button>Get started</Button>
            </Link>
            <Link to="/login">
              <Button variant="outline">Sign in</Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;