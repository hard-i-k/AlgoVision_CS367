import React from 'react';
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  CheckIcon 
} from '@heroicons/react/24/outline';
import { 
  ArrowUpIcon as ArrowUpSolid, 
  ArrowDownIcon as ArrowDownSolid,
  CheckIcon as CheckSolid 
} from '@heroicons/react/24/solid';
import { useQuestionStore } from '../../context/questionStore';
import { useAuthStore } from '../../context/authStore';
import { formatDate } from '../../utils/formatDate';
import Button from '../UI/Button';

const AnswerCard = ({ answer, isQuestionOwner }) => {
  const { voteAnswer, acceptAnswer } = useQuestionStore();
  const { user } = useAuthStore();
  const [userVote, setUserVote] = React.useState(null); // null, 'up', 'down'

  const handleVote = (voteType) => {
    if (!user) return;
    
    // Toggle vote logic
    let newVote = voteType;
    if (userVote === voteType) {
      newVote = null; // Remove vote
    }
    
    voteAnswer(answer.id, newVote || voteType);
    setUserVote(newVote);
  };

  const handleAccept = () => {
    if (isQuestionOwner) {
      acceptAnswer(answer.id);
    }
  };

  return (
    <div className={`bg-white rounded-lg border-2 p-6 ${
      answer.isAccepted 
        ? 'border-green-200 bg-green-50' 
        : 'border-gray-200 hover:border-gray-300'
    } transition-colors`}>
      <div className="flex space-x-4">
        {/* Voting controls */}
        <div className="flex flex-col items-center space-y-2">
          <button
            onClick={() => handleVote('up')}
            disabled={!user}
            className={`p-2 rounded-full transition-colors ${
              userVote === 'up'
                ? 'bg-green-100 text-green-600'
                : 'hover:bg-gray-100 text-gray-600'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {userVote === 'up' ? (
              <ArrowUpSolid className="h-6 w-6" />
            ) : (
              <ArrowUpIcon className="h-6 w-6" />
            )}
          </button>
          
          <span className="text-lg font-semibold text-gray-900">
            {answer.votes}
          </span>
          
          <button
            onClick={() => handleVote('down')}
            disabled={!user}
            className={`p-2 rounded-full transition-colors ${
              userVote === 'down'
                ? 'bg-red-100 text-red-600'
                : 'hover:bg-gray-100 text-gray-600'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {userVote === 'down' ? (
              <ArrowDownSolid className="h-6 w-6" />
            ) : (
              <ArrowDownIcon className="h-6 w-6" />
            )}
          </button>

          {/* Accept button */}
          {isQuestionOwner && !answer.isAccepted && (
            <button
              onClick={handleAccept}
              className="p-2 rounded-full hover:bg-green-100 text-gray-600 hover:text-green-600 transition-colors"
              title="Accept this answer"
            >
              <CheckIcon className="h-6 w-6" />
            </button>
          )}

          {/* Accepted indicator */}
          {answer.isAccepted && (
            <div className="p-2 rounded-full bg-green-100 text-green-600">
              <CheckSolid className="h-6 w-6" />
            </div>
          )}
        </div>

        {/* Answer content */}
        <div className="flex-1 min-w-0">
          {answer.isAccepted && (
            <div className="flex items-center space-x-2 mb-4 text-green-600">
              <CheckSolid className="h-5 w-5" />
              <span className="font-medium text-sm">Accepted Answer</span>
            </div>
          )}

          <div 
            className="prose prose-sm max-w-none mb-6"
            dangerouslySetInnerHTML={{ __html: answer.content }}
          />

          {/* Author and date */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <img
                src={answer.author.avatar}
                alt={answer.author.username}
                className="h-8 w-8 rounded-full"
              />
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {answer.author.username}
                </p>
                <p className="text-xs text-gray-500">
                  answered {formatDate(answer.createdAt)}
                </p>
              </div>
            </div>

            {/* Edit/Delete for answer owner */}
            {user && user.id === answer.author.id && (
              <div className="flex space-x-2">
                <Button variant="ghost" size="sm">
                  Edit
                </Button>
                <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                  Delete
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnswerCard;