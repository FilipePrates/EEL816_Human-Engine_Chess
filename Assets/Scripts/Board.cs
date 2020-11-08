/*
 * Copyright (c) 2018 Razeware LLC
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * Notwithstanding the foregoing, you may not use, copy, modify, merge, publish, 
 * distribute, sublicense, create a derivative work, and/or sell copies of the 
 * Software in any work that is designed, intended, or marketed for pedagogical or 
 * instructional purposes related to programming, coding, application development, 
 * or information technology.  Permission for such use, copying, modification,
 * merger, publication, distribution, sublicensing, creation of derivative works, 
 * or sale is expressly withheld.
 *    
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

using System;
using System.Collections;
using DG.Tweening;
using UnityEngine;

public class Board : MonoBehaviour
{
    public Material defaultMaterial;
    public Material selectedMaterial;
    public float moveSpeed = 2.5f;

    public GameObject AddPiece(GameObject piece, int col, int row)
    {
        Vector2Int gridPoint = Geometry.GridPoint(col, row);
        GameObject newPiece = Instantiate(piece, Geometry.PointFromGrid(gridPoint), Quaternion.identity, gameObject.transform);
        return newPiece;
    }

    public void RemovePiece(GameObject piece)
    {
        Destroy(piece);
    }

    public void MovePiece(GameObject piece, Vector2Int gridPoint)
    {
        MoveSequence(piece, Geometry.PointFromGrid(gridPoint) +  1.5f * Vector3.up)
                .Append(DeselectSequence(piece));
    }

    public void SelectPiece(GameObject piece)
    {
        MeshRenderer renderers = piece.GetComponentInChildren<MeshRenderer>();
        renderers.material = selectedMaterial;
        SelectSequence(piece);
    }

    private Sequence MoveSequence(GameObject piece, Vector3 position)
    {
        Sequence s = DOTween.Sequence();
        s.Append(piece.transform.DOLocalMove(position, .5f));
        return s;
    }

    public void DeselectPiece(GameObject piece, bool cancel)
    {
        MeshRenderer renderers = piece.GetComponentInChildren<MeshRenderer>();
        renderers.material = defaultMaterial;
        if (cancel)
        {
            DeselectSequence(piece);
        }
    }

    private Sequence SelectSequence(GameObject piece)
    {
        Sequence s = DOTween.Sequence();
        s.Append(piece.transform.DOLocalMoveY(1.5f, .5f));
        return s;
    }
    
    private Sequence DeselectSequence(GameObject piece)
    {
        Sequence s = DOTween.Sequence();
        s.Join(piece.transform.DOLocalMoveY(0, .5f));
        return s;
    }

    internal Sequence Rotate()
    {
        Sequence s = DOTween.Sequence();
        var angle = transform.rotation.eulerAngles.y == 0 ? 180 : 0;
        s.Append(transform.DOLocalRotate(new Vector3(0, angle, 0), 1.5f));
        return s;
    }
}
