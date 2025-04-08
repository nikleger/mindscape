import React from 'react';
import {translate} from '@docusaurus/Translate';
import {PageMetadata} from '@docusaurus/theme-common';

interface LastUpdatedProps {
  lastUpdatedAt?: number;
  lastUpdatedBy?: string;
}

export default function LastUpdated({
  lastUpdatedAt,
  lastUpdatedBy,
}: LastUpdatedProps): JSX.Element {
  return (
    <span className="last-updated">
      {lastUpdatedAt && (
        <>
          {translate(
            {
              id: 'theme.lastUpdated.atDate',
              message: 'Last updated at {date}',
              description: 'The label used for the last update time',
            },
            {
              date: new Date(lastUpdatedAt * 1000).toLocaleDateString(),
            },
          )}
          {lastUpdatedBy && (
            <>
              {' '}
              {translate(
                {
                  id: 'theme.lastUpdated.byUser',
                  message: 'by {user}',
                  description: 'The label used for the last update user',
                },
                {
                  user: lastUpdatedBy,
                },
              )}
            </>
          )}
        </>
      )}
    </span>
  );
} 