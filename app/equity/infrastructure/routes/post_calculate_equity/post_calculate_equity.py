from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.equity.infrastructure.routes.post_calculate_equity.calculate_equity_request import CalculateEquityRequest
from app.equity.infrastructure.routes.post_calculate_equity.calculate_equity_response import CalculateEquityResponse
from app.equity.domain.equity_calculator import EquityCalculator
import time
from app.di_container import get_dependency

router = APIRouter(prefix="/v1", tags=["calculate"])


@router.post("/calculate/equity", response_model=CalculateEquityResponse)
async def run(
    request: CalculateEquityRequest,
    calculator: EquityCalculator = Depends(
        lambda: get_dependency("equity_calculator")
    ),
):
    try:
        start = time.time()

        hand_equity, range_equity, tie_equity = calculator.execute(
            request.hand, request.range, request.board
        )
        print(f"Calculation done in {time.time() - start:.2f}s")

        return JSONResponse(
            {
                "hand_equity": hand_equity,
                "range_equity": range_equity,
                "tie_equity": tie_equity,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating the equity of the hand: {str(e)}",
        )
