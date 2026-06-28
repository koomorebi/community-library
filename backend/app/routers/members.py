import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member import Member
from app.models.borrow import Borrow
from app.schemas.member import MemberCreate, MemberUpdate, MemberOut
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/api/v1/members", tags=["会员管理"])


def _generate_card_no(db: Session) -> str:
    while True:
        card_no = f"LIB-{uuid.uuid4().hex[:8].upper()}"
        if not db.query(Member).filter(Member.card_no == card_no).first():
            return card_no


@router.get("", summary="获取会员列表")
def list_members(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Member).filter(Member.is_deleted == False)
    if keyword:
        like = f"%{keyword}%"
        q = q.filter(or_(Member.name.like(like), Member.phone.like(like), Member.card_no.like(like)))

    total = q.count()
    members = q.order_by(Member.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success_response(data={
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [MemberOut.model_validate(m).model_dump() for m in members],
    })


@router.post("", summary="新增会员")
def create_member(req: MemberCreate, db: Session = Depends(get_db)):
    if db.query(Member).filter(Member.phone == req.phone, Member.is_deleted == False).first():
        return error_response(400, "该手机号已注册")

    member = Member(
        name=req.name,
        phone=req.phone,
        id_card=req.id_card,
        address=req.address,
        card_no=_generate_card_no(db),
        max_borrows=req.max_borrows,
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return success_response(data=MemberOut.model_validate(member).model_dump())


@router.get("/{member_id}", summary="获取会员信息")
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id, Member.is_deleted == False).first()
    if not member:
        return error_response(404, "会员不存在")
    return success_response(data=MemberOut.model_validate(member).model_dump())


@router.put("/{member_id}", summary="修改会员")
def update_member(member_id: int, req: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id, Member.is_deleted == False).first()
    if not member:
        return error_response(404, "会员不存在")

    if req.phone and req.phone != member.phone:
        dup = db.query(Member).filter(Member.phone == req.phone, Member.is_deleted == False, Member.id != member_id).first()
        if dup:
            return error_response(400, "该手机号已被使用")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)
    return success_response(data=MemberOut.model_validate(member).model_dump())


@router.delete("/{member_id}", summary="删除会员")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id, Member.is_deleted == False).first()
    if not member:
        return error_response(404, "会员不存在")

    active_borrows = db.query(Borrow).filter(
        Borrow.member_id == member_id, Borrow.status == "borrowed"
    ).count()
    if active_borrows > 0:
        return error_response(400, "该会员有未归还图书，无法删除")

    member.is_deleted = True
    db.commit()
    return success_response(message="删除成功")
