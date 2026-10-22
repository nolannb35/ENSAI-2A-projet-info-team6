from typing import TYPE_CHECKING

from src.DAO.CommentRepo import CommentRepo

if TYPE_CHECKING:
    from src.Model.Comment import Comment


class CommentService:

    def write_comment(self, comment: Comment) -> bool:
        """Allows a user to post a comment.
        Args:
            comment (Comment): Comment to be posted.
        Returns:
            bool: True if posting is sucessfull, false otherwise.
        """
        return CommentRepo().create_comment(comment)
