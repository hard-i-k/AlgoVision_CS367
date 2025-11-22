import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  EyeIcon,
  ShareIcon,
  BookmarkIcon
} from '@heroicons/react/24/outline';
import { 
  ArrowUpIcon as ArrowUpSolid, 
  ArrowDownIcon as ArrowDownSolid 
} from '@heroicons/react/24/solid';
import { useQuestionStore } from '../context/questionStore';
import { useAuthStore } from '../context/authStore';
import AnswerCard from '../components/Answers/AnswerCard';
import AnswerForm from '../components/Answers/AnswerForm';
import Spinner from '../components/UI/Spinner';
import Button from '../components/UI/Button';
import { formatDate } from '../utils/formatDate';

const QuestionDetail = () => {
  const { id } = useParams();
  const { currentQuestion, answers, isLoading, fetchQuestionById, voteQuestion } = useQuestionStore();
  const { user } = useAuthStore();
  const [userVote, setUserVote] = React.useState(null);

  useEffect(() => {
    if (id) {
      fetchQuestionById(id);
    }
  }, [id, fetchQuestionById]);

  const handleVote = (voteType) => {
    if (!user || !currentQuestion) return;
    
    let newVote = voteType;
    if (userVote === voteType) {
      newVote = null;
    }
    
    voteQuestion(currentQuestion.id, newVote || voteType);
    setUserVote(newVote);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Question not found</h1>
        <Link to="/">
          <Button>Back to Questions</Button>
        </Link>
      </div>
    );
  }

  const isQuestionOwner = user && user.id === currentQuestion.author.id;
  const acceptedAnswer = answers.find(answer => answer.isAccepted);
  const otherAnswers = answers.filter(answer => !answer.isAccepted);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Question */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <div className="flex space-x-4">
          {/* Voting controls */}
          <div className="flex flex-col items-center space-y-3">
            <button
              onClick={() => handleVote('up')}
              disabled={!user}
              className={`p-3 rounded-full transition-colors ${
                userVote === 'up'
                  ? 'bg-green-100 text-green-600'
                  : 'hover:bg-gray-100 text-gray-600'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {userVote === 'up' ? (
                <ArrowUpSolid className="h-8 w-8" />
              ) : (
                <ArrowUpIcon className="h-8 w-8" />
              )}
            </button>
            
            <span className="text-2xl font-bold text-gray-900">
              {currentQuestion.votes}
            </span>
            
            <button
              onClick={() => handleVote('down')}
              disabled={!user}
              className={`p-3 rounded-full transition-colors ${
                userVote === 'down'
                  ? 'bg-red-100 text-red-600'
                  : 'hover:bg-gray-100 text-gray-600'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {userVote === 'down' ? (
                <ArrowDownSolid className="h-8 w-8" />
              ) : (
                <ArrowDownIcon className="h-8 w-8" />
              )}
            </button>

            <button className="p-2 rounded-full hover:bg-gray-100 text-gray-600">
              <BookmarkIcon className="h-6 w-6" />
            </button>
          </div>

          {/* Question content */}
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              {currentQuestion.title}
            </h1>

            <div 
              className="prose prose-sm max-w-none mb-6"
              dangerouslySetInnerHTML={{ __html: currentQuestion.description }}
            />

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mb-6">
              {currentQuestion.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
                >
                  {tag}
                </span>
              ))}
            </div>

            {/* Meta info */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <EyeIcon className="h-4 w-4" />
                  <span>{currentQuestion.views} views</span>
                </div>
                <button className="flex items-center space-x-1 hover:text-gray-700">
                  <ShareIcon className="h-4 w-4" />
                  <span>Share</span>
                </button>
              </div>

              <div className="flex items-center space-x-3">
                <img
                  src={currentQuestion.author.avatar}
                  alt={currentQuestion.author.username}
                  className="h-8 w-8 rounded-full"
                />
                <div className="text-sm">
                  <p className="font-medium text-gray-900">
                    {currentQuestion.author.username}
                  </p>
                  <p className="text-gray-500">
                    asked {formatDate(currentQuestion.createdAt)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Answers section */}
      <div className="space-y-6">
        <h2 className="text-xl font-bold text-gray-900">
          {answers.length} {answers.length === 1 ? 'Answer' : 'Answers'}
        </h2>

        {/* Accepted answer first */}
        {acceptedAnswer && (
          <AnswerCard 
            answer={acceptedAnswer} 
            isQuestionOwner={isQuestionOwner}
          />
        )}

        {/* Other answers */}
        {otherAnswers.map((answer) => (
          <AnswerCard 
            key={answer.id} 
            answer={answer} 
            isQuestionOwner={isQuestionOwner}
          />
        ))}

        {/* No answers message */}
        {answers.length === 0 && (
          <div className="text-center py-8 bg-gray-50 rounded-lg">
            <p className="text-gray-600 mb-4">
              No answers yet. Be the first to help!
            </p>
          </div>
        )}

        {/* Answer form */}
        <AnswerForm questionId={id} />
      </div>
    </div>
  );
};

export default QuestionDetail;