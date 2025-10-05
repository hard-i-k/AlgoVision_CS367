import React from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowUpIcon,
  ArrowDownIcon,
  ChatBubbleLeftIcon,
  EyeIcon,
  CheckIcon
} from '@heroicons/react/24/outline';
import { ArrowUpIcon as ArrowUpSolid, ArrowDownIcon as ArrowDownSolid } from '@heroicons/react/24/solid';
import { formatDate } from '../../utils/formatDate';
import { useQuestionStore } from '../../context/questionStore';
import { useAuthStore } from '../../context/authStore';
import Button from '../UI/Button';

const QuestionCard = ({ question }) => {
  const { voteQuestion } = useQuestionStore();
  const { isAuthenticated } = useAuthStore();
  const [userVote, setUserVote] = React.useState(null); // null, 'up', 'down'

  const handleVote = (voteType) => {
    if (!isAuthenticated) return;
    let newVote = voteType;
    if (userVote === voteType) {
      newVote = null;
    }
    voteQuestion(question.id, newVote || voteType);
    setUserVote(newVote);
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex space-x-4">
        {/* Voting and stats */}
        <div className="flex flex-col items-center space-y-2 text-gray-500">
          {/* Upvote button */}
          <button
            onClick={() => handleVote('up')}
            disabled={!isAuthenticated}
            className={`p-2 rounded-full transition-colors mb-1 ${
              userVote === 'up'
                ? 'bg-green-100 text-green-600'
                : 'hover:bg-gray-100 text-gray-600'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
            title={isAuthenticated ? 'Upvote' : 'Sign in to vote'}
          >
            {userVote === 'up' ? (
              <ArrowUpSolid className="h-5 w-5" />
            ) : (
              <ArrowUpIcon className="h-5 w-5" />
            )}
          </button>
          <span className="text-lg font-semibold text-gray-900">{question.votes || 0}</span>
          {/* Downvote button */}
          <button
            onClick={() => handleVote('down')}
            disabled={!isAuthenticated}
            className={`p-2 rounded-full transition-colors mt-1 ${
              userVote === 'down'
                ? 'bg-red-100 text-red-600'
                : 'hover:bg-gray-100 text-gray-600'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
            title={isAuthenticated ? 'Downvote' : 'Sign in to vote'}
          >
            {userVote === 'down' ? (
              <ArrowDownSolid className="h-5 w-5" />
            ) : (
              <ArrowDownIcon className="h-5 w-5" />
            )}
          </button>
          <div className="flex flex-col items-center mt-2">
            <span className={`text-lg font-semibold ${
              (question.answers || 0) > 0 ? 'text-green-600' : 'text-gray-900'
            }`}>
              {question.answers || 0}
            </span>
            <span className="text-xs">answers</span>
          </div>
          <div className="flex flex-col items-center mt-2">
            <span className="text-lg font-semibold text-gray-900">{question.views || 0}</span>
            <span className="text-xs">views</span>
          </div>
        </div>

        {/* Question content */}
        <div className="flex-1 min-w-0">
          <div className="mb-3 flex items-center justify-between">
            <Link
              to={`/questions/${question.id}`}
              className="text-lg font-semibold text-blue-600 hover:text-blue-800 transition-colors"
            >
              {question.title || 'Untitled Question'}
            </Link>
            {/* Reply button */}
            <Link to={`/questions/${question.id}`}>
              <Button size="sm" variant="outline" className="ml-2 flex items-center">
                <ChatBubbleLeftIcon className="h-4 w-4 mr-1" /> Reply
              </Button>
            </Link>
          </div>

          {/* Tags */}
          {question.tags && question.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-3">
              {question.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Author and date */}
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-2">
              {question.author && (
                <>
                  <img
                    src={question.author.avatar || '/default-avatar.png'}
                    alt={question.author.username || 'User'}
                    className="h-6 w-6 rounded-full"
                  />
                  <span>{question.author.username || 'Anonymous'}</span>
                </>
              )}
            </div>
            <span>{question.createdAt ? formatDate(question.createdAt) : 'Unknown date'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionCard;