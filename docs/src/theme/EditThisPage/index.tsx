import React from 'react';
import {translate} from '@docusaurus/Translate';
import {PageMetadata} from '@docusaurus/theme-common';

interface EditThisPageProps {
  editUrl: string;
}

export default function EditThisPage({editUrl}: EditThisPageProps): JSX.Element {
  return (
    <a
      href={editUrl}
      target="_blank"
      rel="noreferrer noopener"
      className="edit-this-page">
      {translate(
        {
          id: 'theme.common.editThisPage',
          message: 'Edit this page',
          description: 'The link label to edit the current page',
        },
        {},
      )}
    </a>
  );
} 