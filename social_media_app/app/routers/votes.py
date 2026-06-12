from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database, oauth2
from sqlmodel import Session, select

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, 
         db: database.Session = Depends(database.get_session), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    #check if the post exists
    post_query = db.exec(select(models.Post_new).where(models.Post_new.id == vote.post_id))
    post_found = post_query.first()

    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {vote.post_id} does not exist")
    
    #check if the user has already voted for the post
    vote_query = db.exec(select(models.Vote).where(models.Vote.post_id == vote.post_id, 
                                                       models.Vote.user_id == current_user.id))
    found_post = vote_query.first()

    if(vote.dir == 1):
        #check if the post exists
        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user with id {current_user.id} has already created a post with id {vote.post_id}")

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()
        return {"message": "vote created successfully"}
    
    else:

        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"vote does not exist")
        
        db.delete(found_post)
        db.commit()
        return {"message": "vote deleted successfully"}